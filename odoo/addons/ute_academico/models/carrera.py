from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UteCarrera(models.Model):
    _name = 'ute.carrera'
    _description = 'Carrera'
    _order = 'name'

    name = fields.Char(string="Carrera", required=True)
