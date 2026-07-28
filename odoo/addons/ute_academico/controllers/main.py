from odoo import http, fields
from odoo.http import request


class AcademicoController(http.Controller):

    @http.route('/academico/ping', type='http', auth='public')
    def ping(self, **kw):
        return request.make_json_response({
            'mensaje': 'El controlador responde correctamente',
            'fecha': fields.Date.today(),
        })
