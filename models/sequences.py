# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class CwmSequence(models.Model):
    _name = 'cwm.sequence'
    _description = 'Sequence'

    def get_sequence(self, seq_name):
        seq = self.env['cwm.sequence'].search([('name', '=', seq_name)])
        if not seq:
            raise UserError(_("Sequence %s not found.") % seq_name)
        if str(seq.suffix) != str(fields.Date.today().year):
            seq.suffix = str(fields.Date.today().year)
            seq.actual_value = 0
            seq.next_value = 0

        sequence = seq.prefix + "-" + str(str(seq.next_value).rjust(5, '0')) + " /" + seq.suffix
        seq.actual_value = seq.next_value
        seq.next_value += 1
        seq.write({'next_value': seq.next_value, 'actual_value': seq.actual_value})
        return sequence


    name = fields.Char(
        string="Seq Name",
        required=True,
        help="Sequence name"
    )
    prefix = fields.Char(
        string="Prefix",
        required=True,
        help="Prefix of the sequence"
    )
    suffix = fields.Char(
        string="Sufix",
        required=True,
        help="Suffix set the actual year"
    )
    actual_value = fields.Integer(
        string="Actual Value",
        required=True,
        help="The last number used"
    )
    next_value = fields.Integer(
        string="Next Value",
        required=True,
        help="The Next value"
    )



