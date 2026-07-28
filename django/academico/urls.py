from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CarreraViewSet, EstudianteViewSet, MatriculaViewSet
from .views import lista_estudiantes, detalle_estudiante

router = DefaultRouter()
router.register(r'carreras', CarreraViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'matriculas', MatriculaViewSet)

urlpatterns = [
    path('', lista_estudiantes, name='home'),
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/<int:pk>/', detalle_estudiante, name='detalle_estudiante'),
    path('api/', include(router.urls)),
]