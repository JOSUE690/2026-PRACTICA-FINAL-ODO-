from odoo import http, fields
from odoo.http import request


class AcademicoController(http.Controller):

    @http.route('/academico/ping', type='http', auth='public')
    def ping(self, **kw):
        return request.make_json_response({
            'mensaje': 'El controlador responde correctamente',
            'fecha': fields.Date.today(),
        })

    @http.route('/academico/api/carreras', type='http', auth='public', csrf=False)
    def carreras(self, **kw):
        carreras = request.env['ute.carrera'].sudo().search([('activa', '=', True)])
        data = []
        for c in carreras:
            data.append({
                'id': c.id,
                'name': c.name,
                'codigo': c.codigo,
                'modalidad': c.modalidad,
            })
        return request.make_json_response(data)

    @http.route('/academico/api/estudiantes', type='http', auth='public', csrf=False)
    def estudiantes(self, **kw):
        estudiantes = request.env['ute.estudiante'].sudo().search([('estado', '=', 'activo')])
        data = []
        for e in estudiantes:
            data.append({
                'id': e.id,
                'name': e.name,
                'cedula': e.cedula,
                'carrera': e.carrera_id.name,
                'estado': e.estado,
            })
        return request.make_json_response(data)

    @http.route('/academico/api/estudiante/<int:estudiante_id>', type='http', auth='public', csrf=False)
    def estudiante_detalle(self, estudiante_id, **kw):
        est = request.env['ute.estudiante'].sudo().browse(estudiante_id)
        if not est.exists():
            return request.make_json_response({'error': 'Estudiante no encontrado'}, status=404)

        matriculas = []
        for m in est.matricula_ids:
            matriculas.append({
                'id': m.id,
                'name': m.name,
                'asignatura': m.asignatura,
                'periodo': m.periodo,
                'estado': m.estado,
                'total': m.total,
            })

        data = {
            'id': est.id,
            'name': est.name,
            'cedula': est.cedula,
            'carrera': est.carrera_id.name,
            'estado': est.estado,
            'matriculas': matriculas,
        }
        return request.make_json_response(data)