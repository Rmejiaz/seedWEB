from django.urls import path
from django.contrib.auth import views as auth_views



from . import views

app_name = 'experimentos'
urlpatterns = [
    path('', views.index, name='index'),
    path('lista_experimentos', views.lista_experimentos, name='lista_experimentos'),
    path('<int:experimento_id>/detalles/', views.ver_experimento, name='ver_experimento'),
    path('<int:experimento_id>/iniciar/', views.iniciar_experimento, name='iniciar_experimento'),
    path('<int:experimento_id>/resultados/', views.mostrar_resultados, name='resultados_experimento'),
    path('cargar_experimento', views.cargar_experimento, name='cargar_experimento'),
    path('<int:experimento_id>/descargar/', views.download_csv, name="descargar_datos")
]