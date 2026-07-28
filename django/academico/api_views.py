from rest_framework import serializers, viewsets

from .models import Carrera, Estudiante, Matricula


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'


class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer


class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.select_related('carrera_id').all()
    serializer_class = EstudianteSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = Matricula.objects.select_related('estudiante_id').all()
    serializer_class = MatriculaSerializer
