from django.contrib import admin

from .models import Carrera, Estudiante, Matricula


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'name', 'modalidad', 'duracion_semestres', 'cupo_maximo', 'activa')
    list_filter = ('modalidad', 'activa')
    search_fields = ('name', 'codigo')


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'name', 'carrera_id', 'estado', 'fecha_ingreso')
    list_filter = ('estado', 'carrera_id', 'genero')
    search_fields = ('name', 'cedula', 'email')
    readonly_fields = ('edad',)


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('name', 'estudiante_id', 'asignatura', 'periodo', 'estado', 'creditos', 'total')
    list_filter = ('estado', 'periodo')
    search_fields = ('name', 'asignatura', 'estudiante_id__name')
