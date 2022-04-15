from django.urls import path, re_path
from user.views import *


urlpatterns = [
    path('', UserInfoView.as_view()),
    path('feedback/', FeedbackView.as_view()),
    # path('google/', GoogleLoginView.as_view(), name='google_login'),
    # path('test/', UserTestView.as_view()),
    path('likes/', LikeProdView.as_view()), ### DEVELOPMENT
    path('subcriebe/', SubscriberView.as_view()),
    re_path('reviews/', ProductReviewView.as_view()),
    path('message_close/<slug:uuid>/', edit_message_status, name='edit_message_status'),
    # path('product/vcode<int:vcode>', ProductView.as_view()),
]