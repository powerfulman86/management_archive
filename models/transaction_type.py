# -*- coding: utf-8 -*-

from odoo import models, fields, api
from ast import literal_eval


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
    sequence_code = fields.Char('Code', required=True, size=4)
    archive_count = fields.Integer(compute="count_archive")

    @api.depends('archive_ids')
    def count_archive(self):
        for rec in self:
            rec.archive_count = len(rec.archive_ids.ids)

    def action_view_archive_ids(self):
        action = self.env.ref('management_archive.archive_management_action').read()[0]
        action['domain'] = [('id', 'in', self.archive_ids.ids)]
        action['context'] = {
            'default_transaction_type': self.id,
            'default_form_kanban': True,
        }
        return action

    def _get_action(self, action_xmlid):
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['display_name'] = self.display_name

        default_immediate_tranfer = True
        if self.env['ir.config_parameter'].sudo().get_param('stock.no_default_immediate_tranfer'):
            default_immediate_tranfer = False

        context = {
            'search_default_transaction_type': [self.id],
            'default_transaction_type': self.id,
        }

        action_context = literal_eval(action['context'])
        context = {**action_context, **context}
        action['context'] = context
        return action

    def get_archive(self):
        return self._get_action('management_archive.archive_management_action')

    count_draft = fields.Integer(compute='_compute_picking_count')
    count_done = fields.Integer(compute='_compute_picking_count')
    count_followup = fields.Integer(compute='_compute_picking_count')
    count_reqresponse = fields.Integer(compute='_compute_picking_count')
    count_closed = fields.Integer(compute='_compute_picking_count')

    def _compute_picking_count(self):
        # TDE TODO count picking can be done using previous two
        domains = {
            'count_draft': [('state', '=', 'draft')],
            'count_done': [('state', '=', 'done')],
            'count_followup': [('state', '=', 'followup')],
            'count_reqresponse': [('state', '=', 'reqresponse')],
            'count_closed': [('state', '=', 'closed')],
        }
        for field in domains:
            data = self.env['management.archive'].read_group(domains[field] +
                                                             [('transaction_type', 'in', self.ids)],
                                                             ['transaction_type'], ['transaction_type']
                                                             )
            count = {
                x['transaction_type'][0]: x['transaction_type_count']
                for x in data if x['transaction_type']
            }
            for record in self:
                record[field] = count.get(record.id, 0)

    def get_action_picking_tree_draft(self):
        return self._get_action('management_archive.action_picking_tree_draft')

    def get_action_picking_tree_draft(self):
        return self._get_action('management_archive.action_picking_tree_draft')

    def get_action_picking_tree_done(self):
        return self._get_action('management_archive.action_picking_tree_done')

    def get_action_picking_tree_followup(self):
        return self._get_action('management_archive.action_picking_tree_followup')

    def get_action_picking_tree_reqresponse(self):
        return self._get_action('management_archive.action_picking_tree_reqresponse')

    def get_action_picking_tree_close(self):
        return self._get_action('management_archive.action_picking_tree_close')
