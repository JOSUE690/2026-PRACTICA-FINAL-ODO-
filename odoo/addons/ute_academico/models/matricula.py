from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UteMatricula(models.Model):
    _name = 'ute.matricula'
    _description = 'Matrícula'

    name = fields.Char(string="Número", required=True)
    estudiante_id = fields.Many2one('ute.estudiante', required=True, ondelete='cascade')
    periodo = fields.Selection([
        ('2026-01', '2026-01'),
        ('2026-02', '2026-02'),
    ], required=True)
    asignatura = fields.Char(required=True)
    creditos = fields.Integer(default=3)
    costo_credito = fields.Float(default=25.0)
    total = fields.Float(compute='_compute_total', store=True)
    fecha = fields.Date(default=fields.Date.today)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('anulada', 'Anulada'),
    ], default='borrador')
    observacion = fields.Text()

    @api.depends('creditos', 'costo_credito')
    def _compute_total(self):
        for r in self:
            r.total = r.creditos * r.costo_credito

    @api.constrains('creditos')
    def _check_creditos(self):
        for r in self:
            if r.creditos < 1 or r.creditos > 6:
                raise ValidationError('Los créditos deben ser entre 1 y 6.')

    def action_confirmar(self):
        for r in self:
            if r.estado != 'borrador':
                raise ValidationError('Solo se puede confirmar una matrícula en borrador.')
            r.estado = 'confirmada'

    def action_anular(self):
        for r in self:
            if r.estado == 'anulada':
                raise ValidationError('La matrícula ya está anulada.')
            r.estado = 'anulada'