from django.urls import path
from django.contrib.auth import views as auth_views



from . import views

app_name = 'test'
urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('captures', views.captures, name='captures'),
    path('captures_results', views.captures_results, name='captures_results'),
    path('accounts/login/', auth_views.LoginView.as_view()),
]