# -*- coding: utf-8 -*-
{
    'name': "Management Archiving",

    'summary': """
        Custom Application To enhance document mailing service
        """,

    'description': """
        upload management archiving data 
    """,

    'author': "SIIC",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Other',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'contacts'],

    # always loaded
    'images': ['static/description/icon.png'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/management_archive_view.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/archive_icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
