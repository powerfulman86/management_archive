# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

AVAILABLE_STATUS = [
    ('draft', 'Draft'),
    ('lock', 'Locked'),
    ('followup', 'Follow Up'),
    ('reqresponse', 'Request Response'),
    ('closed', 'Closed'),
]


class ManagementArchive(models.Model):
    _name = 'management.archive'
    _description = 'Management Archive'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    issue_date = fields.Date(string='Issue Date', default=fields.Date.context_today, copy=False)
    name = fields.Char(string='Document Number', required=False, copy=False)
    transaction_id = fields.Char('Transaction Id', index=True, size=10)
    transaction_type = fields.Many2one(comodel_name="transaction.type", string="Transaction Type", required=True, )
    state = fields.Selection(AVAILABLE_STATUS, string='state', tracking=True, default=AVAILABLE_STATUS[0][0],
                             required=True)

    child_ids = fields.One2many(comodel_name='management.archive', inverse_name='parent_id')
    parent_id = fields.Many2one(comodel_name='management.archive', string='Parent')
    next = fields.Integer('Next child sequence')
    children_count = fields.Integer('count', compute="compute_children_count")

    @api.depends('child_ids')
    def compute_children_count(self):
        for rec in self:
            rec.children_count = len(rec.child_ids.ids)

    def action_view_children(self):
        self.ensure_one()
        action = self.env.ref('management_archive.archive_management_action')
        result = action.read()[0]
        result['context'] = {'default_parent_id': self.id }
        result['domain'] = "[('id', 'in', " + str(self.child_ids.ids) + ")]"
        return result

    partner_id = fields.Many2one('management.archive.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)], 'lock': [('readonly', True)]},
                                 required=True, index=True, tracking=1, )
    subject = fields.Text('Subject')
    default_description = fields.Html('Description', help='Description')
    signature_key = fields.Many2one('management.signature.key', invisible=1, copy=False)
    signature_desc = fields.Text('Note')
    signature_date = fields.Date(string="Signature Date", tracking=True, default=fields.Date.context_today, copy=False)
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_rel2', 'doc_id', 'attach_id3',
                                         string="Attachment",
                                         help='You can attach the copy of your document', copy=False, attachment=True)
    priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', index=True,
                                default=AVAILABLE_PRIORITIES[0][0])
    form_kanban = fields.Boolean("")
    _sql_constraints = [
        (
            "transaction_id_unique",
            "unique(transaction_id)",
            "Archive Transaction Id must be unique across the database!",
        )
    ]

    def action_approve(self):
        self.state = 'lock'

    def action_followup(self):
        self.state = 'followup'

    def action_request_response(self):
        self.state = 'reqresponse'

    def action_close(self):
        self.state = 'closed'

    def reset_draft(self):
        self.state = 'draft'

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("لا يمكن حذف مكاتبه تم اعتمادها"))
        return super(ManagementArchive, self).unlink()

    @api.model
    def create(self, values):
        res = super(ManagementArchive, self).create(values)
        seq = self.env['ir.sequence'].next_by_code('management.archive') or '/'
        currentYear = datetime.now().year
        name = str(res['transaction_type'].sequence_code) + "-" + str(currentYear) + "-" + str(seq)
        res['name'] = name
        if res.parent_id:
            res.parent_id.next +=1
            res['name'] =res['name']+"-"+str(res.parent_id.next).zfill(3)
        return res


class ManagementArchivePartner(models.Model):
    _name = 'management.archive.partner'
    _rec_name = "partner_id"
    _description = 'Management Archive Partner'

    partner_id = fields.Many2one('res.partner', required=True)
    note = fields.Text('Description')
