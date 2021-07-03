# -*- coding: utf-8 -*-
{
    'name': "Management Archiving",
    'summary': """  Custom Application To enhance document mailing service """,
    'description': """ upload management archiving data  """,
    'author': "SIIC",
    'category': 'Other',
    'depends': ['base', 'portal', 'contacts', 'utm'],
    'images': ['static/description/icon.png'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/management_archive_view.xml',
        'views/transaction_type_view.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
