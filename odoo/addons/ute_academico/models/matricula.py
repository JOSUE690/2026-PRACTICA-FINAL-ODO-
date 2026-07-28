from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UteMatricula(models.Model):
    _name = 'ute.matricula'
    _description = 'Matrícula'
    _order = 'id desc'

    name = fields.Char(string="Número", required=True)
