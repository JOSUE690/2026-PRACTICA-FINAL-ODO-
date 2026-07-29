from django.core.management.base import BaseCommand
from academico.models import Carrera, Estudiante, Matricula
from datetime import date


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para el proyecto académico'

    def handle(self, *args, **options):
        Carrera.objects.all().delete()
        Estudiante.objects.all().delete()
        Matricula.objects.all().delete()

        carrera1 = Carrera.objects.create(
            name='Ingeniería en Sistemas',
            codigo='ISG001',
            modalidad='presencial',
            duracion_semestres=8,
            cupo_maximo=40,
            activa=True,
        )
        carrera2 = Carrera.objects.create(
            name='Administración',
            codigo='ADM001',
            modalidad='online',
            duracion_semestres=6,
            cupo_maximo=35,
            activa=True,
        )

        estudiantes = [
            {'name': 'Ana Torres', 'cedula': '0923456789', 'email': 'ana@example.com', 'carrera': carrera1, 'estado': 'activo'},
            {'name': 'Luis Pérez', 'cedula': '0987654321', 'email': 'luis@example.com', 'carrera': carrera2, 'estado': 'activo'},
            {'name': 'María López', 'cedula': '0900000001', 'email': 'maria@example.com', 'carrera': carrera1, 'estado': 'egresado'},
            {'name': 'Carlos Ruiz', 'cedula': '0911111111', 'email': 'carlos@example.com', 'carrera': carrera2, 'estado': 'retirado'},
        ]

        created_estudiantes = []
        for data in estudiantes:
            created_estudiantes.append(Estudiante.objects.create(
                name=data['name'],
                cedula=data['cedula'],
                email=data['email'],
                carrera_id=data['carrera'],
                fecha_ingreso=date(2024, 9, 1),
                estado=data['estado'],
            ))

        matriculas = [
            {'name': 'MAT-001', 'estudiante': created_estudiantes[0], 'periodo': '2026-01', 'asignatura': 'Programación', 'creditos': 3, 'estado': 'confirmada'},
            {'name': 'MAT-002', 'estudiante': created_estudiantes[0], 'periodo': '2026-01', 'asignatura': 'Bases de Datos', 'creditos': 4, 'estado': 'borrador'},
            {'name': 'MAT-003', 'estudiante': created_estudiantes[1], 'periodo': '2026-02', 'asignatura': 'Contabilidad', 'creditos': 3, 'estado': 'confirmada'},
            {'name': 'MAT-004', 'estudiante': created_estudiantes[2], 'periodo': '2026-02', 'asignatura': 'Redes', 'creditos': 2, 'estado': 'anulada'},
            {'name': 'MAT-005', 'estudiante': created_estudiantes[3], 'periodo': '2026-01', 'asignatura': 'Investigación', 'creditos': 4, 'estado': 'confirmada'},
        ]

        for data in matriculas:
            Matricula.objects.create(
                name=data['name'],
                estudiante_id=data['estudiante'],
                periodo=data['periodo'],
                asignatura=data['asignatura'],
                creditos=data['creditos'],
                costo_credito='25.00',
                estado=data['estado'],
            )

        self.stdout.write(self.style.SUCCESS('Datos cargados correctamente'))
