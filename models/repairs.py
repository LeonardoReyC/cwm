# -*- coding: utf-8 -*-

#TODO odoo.odoo
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CwmRepair(models.Model):
    _name = 'cwm.repair'

    name = fields.Char(
        string='Description'
    )
    sequence = fields.Many2one(
        comodel_name='cwm.sequence',
        string='Sequence',
        default=lambda self: self.env['cwm.sequence'].search([('name', '=', 'Repairs')], limit=1)
    )
    rep_num = fields.Char(
        string='OR',
        readonly=True
    )
    car_id = fields.Many2one(
        comodel_name='cwm.car',
        string="Car",
        required=True,
    )
    budget = fields.Monetary(
        string="Budget",
        currency_field="currency_id"
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.EUR')
    )
    """
    worker_ids = fields.Many2many(
        comodel_name='cwm.workers',
        string='Workers'
    )
    """

    @api.model
    def create(self, vals):
        seq_name = 'Repairs'
        sequence = self.env['cwm.sequence'].search([('name', '=', seq_name)], limit=1)
        if not sequence:
            raise UserError(_("Sequence %s not found.") % seq_name)
        vals['rep_num'] = sequence.get_sequence(seq_name)
        vals['sequence'] = sequence.id
        return super(CwmRepair, self).create(vals)


#TODO Implementación secuencia antes de continuar
