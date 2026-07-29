from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UteCarrera(models.Model):
    _name = 'ute.carrera'
    _description = 'Carrera'

    name = fields.Char(string="Carrera", required=True)
    codigo = fields.Char(string="Código", required=True)
    modalidad = fields.Selection([
        ('presencial', 'Presencial'),
        ('semipresencial', 'Semipresencial'),
        ('online', 'Online'),
    ], default='presencial')
    duracion_semestres = fields.Integer(default=8)
    cupo_maximo = fields.Integer(default=40)
    activa = fields.Boolean(default=True)
    estudiante_ids = fields.One2many('ute.estudiante', 'carrera_id')
    total_estudiantes = fields.Integer(compute='_compute_total_estudiantes', store=True)

    _sql_constraints = [
        ('codigo_unique', 'unique(codigo)', 'El código ya existe.'),
    ]

    @api.depends('estudiante_ids.estado')
    def _compute_total_estudiantes(self):
        for r in self:
            r.total_estudiantes = len(r.estudiante_ids.filtered(lambda e: e.estado == 'activo'))

    @api.constrains('duracion_semestres')
    def _check_duracion(self):
        for r in self:
            if r.duracion_semestres < 4 or r.duracion_semestres > 12:
                raise ValidationError('La duración debe ser entre 4 y 12 semestres.')

    @api.constrains('cupo_maximo')
    def _check_cupo(self):
        for r in self:
            if r.cupo_maximo <= 0:
                raise ValidationError('El cupo debe ser mayor a 0.')