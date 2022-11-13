from django.urls import path

from . import views

app_name = 'test'
urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('captures', views.captures, name='captures'),
]