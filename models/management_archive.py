# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ManagementArchive(models.Model):
    _name = 'management.archive'
    _description = 'Management Archive'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    issue_date = fields.Date(string='Issue Date', default=fields.Date.context_today, copy=False)
    name = fields.Char(string='Document Number', required=True, copy=False)
    transaction_id = fields.Char('Transaction Id', index=True)
    transaction_type = fields.Many2one(comodel_name="transaction.type", string="Transaction Type", required=True, )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Locked')])
    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'done': [('readonly', True)]},
        required=True, index=True, tracking=1,)
    subject = fields.Text('Subject')
    signature_key = fields.Many2one('management.signature.key', invisible=1, copy=False, required=True)
    signature_desc = fields.Text('Note')
    signature_date = fields.Date(string="Signature Date", default=fields.Date.context_today, copy=False)
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False, attachment=True)
    _sql_constraints = [
        (
            "transaction_id_unique",
            "unique(transaction_id)",
            "Archive Transaction Id must be unique across the database!",
        )
    ]

