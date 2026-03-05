from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from . import api

app_name = 'encuestas'

router = DefaultRouter()
router.register(r'api/preguntas', api.PreguntaViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pregunta_id>/', views.detalle, name='detalle'),
    path('<int:pregunta_id>/votar/', views.votar, name='votar'),
    path('<int:pregunta_id>/resultados/', views.resultados, name='resultados'),
    path('<int:pregunta_id>/exportar/', views.exportar_resultados_csv, name='exportar'),
]

urlpatterns += router.urls