from django.urls import path
from django.contrib.auth import views as auth_views



from . import views

app_name = 'experimentos'
urlpatterns = [
    path('', views.index, name='index'),
    path('lista_experimentos', views.lista_experimentos, name='lista_experimentos'),
    path('<int:experimento_id>/detalles/', views.ver_experimento, name='ver_experimento'),
]