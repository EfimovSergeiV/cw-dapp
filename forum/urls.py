from django.urls import path
from forum.views import *

urlpatterns = [
    path('cts/', CategoryView.as_view()),
    path('topics/', TopicsView.as_view()),
    path('topic/', TopicView.as_view()),
    path('posts/', PostsView.as_view()),
]
