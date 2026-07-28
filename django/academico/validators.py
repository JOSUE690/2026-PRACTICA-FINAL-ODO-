from django.core.exceptions import ValidationError

def validar_cedula(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError('La cédula debe tener exactamente 10 dígitos numéricos.')