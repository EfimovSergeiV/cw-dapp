from rest_framework.views import APIView
from rest_framework.response import Response
from forum.models import *
from forum.serializer import *


class CategoryView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        qs = CategoryModel.objects.filter(activated=True)
        serializer = self.serializer_class(qs, many=True, context={'request':request})

        return Response(serializer.data)


class TopicsView(APIView):
    serializer_class = TopicSerializer

    def get(self, request):
        qs = TopicModel.objects.filter(category_id=1)
        serializer = self.serializer_class(qs, many=True, context={'request':request})

        return Response(serializer.data)


class TopicView(APIView):
    serializer_class = TopicSerializer

    def get(self, request):
        qs = TopicModel.objects.get(id=1)
        serializer = self.serializer_class(qs, context={'request':request})

        return Response(serializer.data)


class PostsView(APIView):
    serializer_class = PostsSerializer

    def get(self, request):
        qs = PostModel.objects.filter(topic_id=1)
        serializer = self.serializer_class(qs, many=True, context={'request':request})

        return Response(serializer.data)