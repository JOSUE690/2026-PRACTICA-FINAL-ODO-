from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Carrera, Estudiante, Matricula


class AcademicoModelTests(TestCase):
    def setUp(self):
        self.carrera = Carrera.objects.create(
            name='Ingeniería en Sistemas',
            codigo='ISG001',
            modalidad='presencial',
            duracion_semestres=8,
            cupo_maximo=40,
        )
        self.estudiante = Estudiante.objects.create(
            name='Ana Torres',
            cedula='0923456789',
            email='ana@example.com',
            telefono='0999999999',
            fecha_nacimiento=date(2000, 1, 15),
            genero='F',
            carrera_id=self.carrera,
            fecha_ingreso=date(2024, 9, 1),
            estado='activo',
            notas='Buen desempeño',
        )
        self.matricula = Matricula.objects.create(
            name='MAT-001',
            estudiante_id=self.estudiante,
            periodo='2026-01',
            asignatura='Programación',
            creditos=3,
            costo_credito='25.00',
            estado='borrador',
            observacion='Pendiente de pago',
        )

    def test_total_estudiantes_de_carrera(self):
        self.assertEqual(self.carrera.total_estudiantes, 1)

    def test_edad_del_estudiante(self):
        hoy = date.today()
        esperado = hoy.year - self.estudiante.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.estudiante.fecha_nacimiento.month, self.estudiante.fecha_nacimiento.day)
        )
        self.assertEqual(self.estudiante.edad, esperado)

    def test_total_de_matricula(self):
        self.assertEqual(self.matricula.total, 75.0)


class AcademicoViewTests(TestCase):
    def setUp(self):
        self.carrera = Carrera.objects.create(
            name='Administración',
            codigo='ADM001',
            modalidad='online',
        )
        self.estudiante = Estudiante.objects.create(
            name='Luis Pérez',
            cedula='0987654321',
            email='luis@example.com',
            carrera_id=self.carrera,
            fecha_ingreso=date(2023, 8, 1),
        )

    def test_lista_estudiantes_muestra_alumno(self):
        response = self.client.get(reverse('lista_estudiantes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.estudiante.name)

    def test_detalle_estudiante_muestra_datos(self):
        response = self.client.get(reverse('detalle_estudiante', kwargs={'pk': self.estudiante.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.estudiante.cedula)
