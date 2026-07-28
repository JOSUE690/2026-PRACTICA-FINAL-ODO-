from django.shortcuts import get_object_or_404, render

from .models import Estudiante


def lista_estudiantes(request):
    estudiantes = Estudiante.objects.select_related('carrera_id').all()
    return render(request, 'academico/lista_estudiantes.html', {'estudiantes': estudiantes})


def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante.objects.select_related('carrera_id'), pk=pk)
    return render(request, 'academico/detalle_estudiante.html', {'estudiante': estudiante})
