from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class UteEstudiante(models.Model):
    _name = 'ute.estudiante'
    _description = 'Estudiante'

    name = fields.Char(string="Nombres y apellidos", required=True)
    cedula = fields.Char(required=True)
    email = fields.Char()
    telefono = fields.Char()
    fecha_nacimiento = fields.Date()
    edad = fields.Integer(compute='_compute_edad')
    genero = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ])
    carrera_id = fields.Many2one('ute.carrera', required=True, ondelete='restrict')
    modalidad = fields.Selection(related='carrera_id.modalidad')
    fecha_ingreso = fields.Date(default=fields.Date.today)
    estado = fields.Selection([
        ('activo', 'Activo'),
        ('egresado', 'Egresado'),
        ('retirado', 'Retirado'),
    ], default='activo')
    matricula_ids = fields.One2many('ute.matricula', 'estudiante_id')
    notas = fields.Text()

    _sql_constraints = [
        ('cedula_unique', 'unique(cedula)', 'Ya existe un estudiante con esa cédula.'),
    ]

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        for r in self:
            if r.fecha_nacimiento:
                hoy = date.today()
                fn = r.fecha_nacimiento
                r.edad = hoy.year - fn.year - ((hoy.month, hoy.day) < (fn.month, fn.day))
            else:
                r.edad = 0

    @api.constrains('cedula')
    def _check_cedula(self):
        for r in self:
            if not r.cedula.isdigit() or len(r.cedula) != 10:
                raise ValidationError('La cédula debe tener 10 dígitos numéricos.')

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for r in self:
            if r.fecha_nacimiento and r.fecha_nacimiento > date.today():
                raise ValidationError('La fecha de nacimiento no puede ser futura.')