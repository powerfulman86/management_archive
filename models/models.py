# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SignatureKey(models.Model):
    _name = 'management.signature.key'
    _description = 'Management Signature Key'

    name = fields.Char('Name')
    note = fields.Text('Note')
    active = fields.Boolean('Active', default=True,
                            help="Set active to false to hide the signature key Plan without removing it.")

