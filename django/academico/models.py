from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from .validators import validar_cedula

class Carrera(models.Model):
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('online', 'Online'),
    ]

    name = models.CharField(max_length=100)
    codigo = models.CharField(max_length=6, unique=True)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES, default='presencial')
    duracion_semestres = models.PositiveSmallIntegerField(
        default=8, 
        validators=[MinValueValidator(4), MaxValueValidator(12)]
    )
    cupo_maximo = models.PositiveIntegerField(
        default=40, 
        validators=[MinValueValidator(1)]
    )
    activa = models.BooleanField(default=True)

    @property
    def total_estudiantes(self):
        return self.estudiantes.filter(estado='activo').count()

    def __str__(self):
        return f"{self.codigo} - {self.name}"

    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['name']


class Estudiante(models.Model):
    GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    ESTADO_CHOICES = [('activo', 'Activo'), ('egresado', 'Egresado'), ('retirado', 'Retirado')]

    name = models.CharField(max_length=120)
    cedula = models.CharField(max_length=10, unique=True, validators=[validar_cedula])
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True)
    carrera_id = models.ForeignKey(Carrera, on_delete=models.PROTECT, related_name='estudiantes')
    fecha_ingreso = models.DateField(default=date.today)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    notas = models.TextField(blank=True)

    @property
    def modalidad(self):
        return self.carrera_id.modalidad

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return 0
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __str__(self):
        return f"{self.cedula} - {self.name}"

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['name']


class Matricula(models.Model):
    PERIODO_CHOICES = [('2026-01', '2026-01'), ('2026-02', '2026-02')]
    ESTADO_CHOICES = [('borrador', 'Borrador'), ('confirmada', 'Confirmada'), ('anulada', 'Anulada')]

    name = models.CharField(max_length=20)
    estudiante_id = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='matriculas')
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES)
    asignatura = models.CharField(max_length=100)
    creditos = models.PositiveSmallIntegerField(
        default=3, 
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    costo_credito = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=25.00, 
        validators=[MinValueValidator(0.01)]
    )
    fecha = models.DateField(default=date.today)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='borrador')
    observacion = models.TextField(blank=True)

    @property
    def total(self):
        return float(self.creditos) * float(self.costo_credito)

    def __str__(self):
        return f"{self.name} - {self.asignatura}"

    class Meta:
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['-fecha']