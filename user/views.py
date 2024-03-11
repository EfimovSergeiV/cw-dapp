from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.conf import settings
from main.agent import send_alert_to_agent

from user import serializers
from user.models import *
from django.shortcuts import render


""" Редактирование статуса сообщений пользователей """
def edit_message_status(request, uuid):
    qs = FeedBackModel.objects.filter(uuid=uuid)
    
    try:
        if len(qs) == 1 and request.headers['Cookie']:
            if qs[0].completed:
                post = f"Вопрос клиента { qs[0].person } кто-то уже взял на себя"
            else:
                qs.update(completed=True)
                post = f"Вопрос клиента { qs[0].person } помечен как закрытый"
                send_alert_to_agent(oth_status = { "client": qs[0].person })
        else:
            post = "Вопрос не найден в системе"

        return render(request, 'questionclosed.html', { 'post': post })
    except:
        post = "Вы не прошли проверку на работа"
        return render(request, 'questionclosed.html', { 'post': post })


class UserTestView(APIView):
    """ Пользователь """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response('SUCCESS')


class UserInfoView(APIView):
    """ Информация о пользователе """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user.username
        return Response(user)


class SubscriberView(APIView):
    """ Подписаться на новости """

    def get(self, request):
        qs = SubscriberModel.objects.get(id=1)
        sr = serializers.SubscriberSerializer(qs)
        return Response(sr.data)

    def post(self, request):
        sr = serializers.SubscriberSerializer(data=request.data)
        exist = SubscriberModel.objects.filter(email=request.data['email']).exists()
        if exist:
            return Response({"success": "Пользователь подписан"})
        else:
            if sr.is_valid():
                sr.save()
                # return Response({"exist": "Пользователь существует"})
                return Response({"success": "Пользователь подписан"})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)



# class GoogleLoginView(SocialLoginView):
#     authentication_classes = [] # disable authentication
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = "http://localhost:3000/login"
#     client_class = OAuth2Client


class LikeProdView(APIView):
    """ Избранные товары пользователя """

    permission_classes = [permissions.IsAuthenticated, ]
    sr_like = serializers.LikesProductsSR
    sr_like_detail = serializers.LikeProductDetailSR

    def action(self, request, format=None):

        request.data['user'] = request.user.id
        serializer = self.sr_like(data=request.data)
        liked_product = LikeProdModel.objects.filter(
            user=request.user.id, product=request.data['product']
        )

        if not liked_product and serializer.is_valid():
            serializer.save()
            return status.HTTP_201_CREATED
        if liked_product and serializer.is_valid():
            liked_product.delete()
            return status.HTTP_200_OK
        return status.HTTP_400_BAD_REQUEST

    def get(self, request):
        like_prod = LikeProdModel.objects.filter(user=request.user.id)
        sr = self.sr_like_detail(like_prod, many=True, context={'request':request})
        return Response(sr.data)

    def post(self, request,):
        return Response(
            status=self.action(request)
        )

    def delete(self, request,):
        return Response(
            status=self.action(request)
        )


class ProductReviewView(APIView):
    """ Отзывы клиентов о товарах """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        prod_id = self.request.query_params.get('prod_id')
        try:
            reviews = ProductReviewModel.objects.filter(visible=True, product=int(prod_id))
        except ValueError and TypeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ProductReviewSR(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        # request.data['user'] = request.user.id   Подставлять имя из базы юзеров, если пользователь авторизован
        serializer = serializers.MainProductReviewSR(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FeedbackView(APIView):
    """ Обратная связь с общей формы сообщений """

    def post(self, request):
        
        resp = { "success": "Спасибо за Ваше сообщение! Мы свяжемся с Вами в ближайшее время!" }
        serializer = serializers.FeedBackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            send_alert_to_agent(message=serializer.data)
        else:
            resp = { "danger": "Что то пошло не так( Попробуте позже." }

        return Response(resp)
    



from user.serializers import UserWatcherSerializer, UserWatcherUUIDSerializer
from django.db.models import Case, When
from django.db.models import Count, F, Value

def preserved(prods):
    return Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(prods)])

class UserWatcherView(APIView):
    """ Пользовательская статистика """

    def get(self, request):
        """ Возвращаем историю последних просмотров товаров """

        if request.headers.get('Authorization'):
            userwatcher_qs = UserWatcherModel.objects.filter(tmp_id=request.headers.get('Authorization'))

            # WTF?!
            if userwatcher_qs.exists() == False:
                data = { "tmp_id": request.headers.get('Authorization')}
                sr = UserWatcherUUIDSerializer(data=data)
                
                if sr.is_valid():
                    sr.save()
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)


            tmp_qs = userwatcher_qs[0]
            tmp_data = tmp_qs.prods

            if tmp_data:
                prods_qs = ProductModel.objects.filter(id__in = tmp_data["viewed"] + tmp_data["like"] + tmp_data["comp"])

                sr = UserWatcherSerializer(
                    {
                        "viewed": prods_qs.filter(id__in = tmp_data["viewed"]).order_by(preserved(tmp_data["viewed"])),
                        "like": prods_qs.filter(id__in = tmp_data["like"]).order_by(preserved(tmp_data["like"])),
                        "comp": prods_qs.filter(id__in = tmp_data["comp"]).order_by(preserved(tmp_data["comp"])),
                    },
                    context = { 'request': request }
                )

                return Response(sr.data)
            else:
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def post(self, request):
        """ Обновляем информацию о просмотренных товарах """

        if request.headers.get('Authorization'):
            qs = UserWatcherModel.objects.filter(tmp_id=request.headers.get('Authorization'))

            if qs:  # Если tmp_id был удалён в активной сессии вручную, то в текущей сессии ошибка
                for key in request.data.keys():
                    current_data = qs[0].prods if qs[0].prods else { "comp": [], "like": [], "viewed": [] }
                    current_data[key] = [request.data.get(key),] + current_data[key][0:11] if request.data.get(key) not in current_data[key] else current_data[key]
                    qs.update(updatedAt=timezone.now(), prods=current_data)

        return Response(status=status.HTTP_201_CREATED)
    

    def delete(self, request):
        if request.headers.get('Authorization'):
            qs = UserWatcherModel.objects.filter(tmp_id=request.headers.get('Authorization'))
            for key in request.data.keys():
                current_data = qs[0].prods
                try:
                    current_data[key].remove(request.data.get(key))
                    qs.update(prods=current_data)
                except ValueError:
                    pass

        return Response(status=status.HTTP_200_OK)


    def put(self, request):
        """ 
            1. Получаем новый или обновляем идентификатор
            2. Заодно сначало почистим UUID's с чистой историей
        """
        print('update')

        empty_tmp_prods = UserWatcherModel.objects.filter(models.Q(prods__isnull=True) | models.Q(prods__exact={})) #.filter(prods=Value('None'))
        empty_tmp_prods.delete()

        if request.data.get('tmp_id'):
            tmp_exist = UserWatcherModel.objects.filter(tmp_id=request.data.get('tmp_id')).exists()
            if tmp_exist == False:
                qs = UserWatcherModel.objects.create()
                return Response({ "tmp_id": qs.tmp_id })
            else:
                return Response(status=status.HTTP_200_OK)
        else:
            qs = UserWatcherModel.objects.create()
            return Response({ 'tmp_id': qs.tmp_id })



class UserSessionView(APIView):
    """ Привязка сессии к пользователю """
    
    permission_classes = [ permissions.IsAuthenticated, ]
    
    def post(self, request):
        user_qs = User.objects.get(username=request.user)
        profile_qs = ProfileModel.objects.filter(user=user_qs)

        # Проверяем, есть ли у пользователя профайл, нет? Создаём.        
        if profile_qs.exists() == False:
            ProfileModel.objects.create(user=user_qs, latest_session = request.data.get('tmp_id'))

        # Если нет последней сессии, то делаем текущую последней
        if profile_qs[0].latest_session == None:
            profile_qs.update(latest_session = request.data.get('tmp_id'))
        
        # Если последняя сессия удалена из архива сессий, создаём её снова
        elif UserWatcherModel.objects.filter(tmp_id = user_qs.user_profile.latest_session).exists() == False:
            profile_qs = ProfileModel.objects.get(user=user_qs)
            data = { "tmp_id": profile_qs.latest_session}
            sr = UserWatcherUUIDSerializer(data=data)
                
            if sr.is_valid():
                sr.save()

            return Response({ "tmp_id": request.data.get('tmp_id') })

        return Response({ "tmp_id": user_qs.user_profile.latest_session })


# "GET /c/prod/lk HTTP/1.1" 404 7632 Err при входе, повторно норм
from user.serializers import DataUserOrdersSerializer
class DataUserOrdersView(APIView):
    """ Дополнительная информация о пользователе """
    
    def get(self, request):
        try:
            user_qs = User.objects.get(username=request.user)
            profile_qs = ProfileModel.objects.get(user=user_qs)
            sr = DataUserOrdersSerializer(profile_qs, context={'request':request})

            return Response(sr.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)