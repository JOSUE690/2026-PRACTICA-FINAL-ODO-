{
    'name': "Gestión Académica UTE",
    'summary': "Examen final Programación II - Carreras, Estudiantes y Matrículas",
    'author': "APELLIDO NOMBRE",
    'website': "https://www.ute.edu.ec",
    'category': 'Education',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/carrera_views.xml',
        'views/estudiante_views.xml',
        'views/matricula_views.xml',
        'views/menus.xml',
        'demo/demo.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}