# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TransactionType(models.Model):
    _name = 'transaction.type'
    _description = 'Archive Transaction Types'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Name')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True,
                            help="Set active to false to hide the Medical Plan without removing it.")
    color = fields.Integer('Color')
    sequence = fields.Integer('Sequence', help="Used to order the 'All Operations' kanban view")
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence', copy=False)
    sequence_code = fields.Char('Code', required=True)
