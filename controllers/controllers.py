# -*- coding: utf-8 -*-
# from odoo import http


# class ManagemengtArchive(http.Controller):
#     @http.route('/managemengt_archive/managemengt_archive/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/managemengt_archive/managemengt_archive/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('managemengt_archive.listing', {
#             'root': '/managemengt_archive/managemengt_archive',
#             'objects': http.request.env['managemengt_archive.managemengt_archive'].search([]),
#         })

#     @http.route('/managemengt_archive/managemengt_archive/objects/<model("managemengt_archive.managemengt_archive"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('managemengt_archive.object', {
#             'object': obj
#         })
