from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UteEstudiante(models.Model):
    _name = 'ute.estudiante'
    _description = 'Estudiante'
    _order = 'name'

    name = fields.Char(string="Nombres y apellidos", required=True)
