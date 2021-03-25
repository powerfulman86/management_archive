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
    archive_ids = fields.One2many(comodel_name='management.archive', inverse_name='transaction_type')
    sequence = fields.Integer('Sequence', help="Used to order the 'All Operations' kanban view")
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence', copy=False)
    sequence_code = fields.Char('Code', required=True)
    archive_count = fields.Integer(compute="count_archive")

    @api.depends('archive_ids')
    def count_archive(self):
        for rec in self:
            rec.archive_count = len(rec.archive_ids.ids)

    def action_view_archive_ids(self):
        action = self.env.ref('managemengt_archive.archive_management_action').read()[0]
        action['domain'] = [('id', 'in', self.archive_ids.ids)]
        action['context'] = {
            'default_transaction_type': self.id,
        }
        return action
