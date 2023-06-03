# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CwmRates(models.Model):
    _name = 'cwm.rates'
    _description = 'Aplicable rates'

    name = fields.Char(
        string="Aplicable to",
        required=True,
        help="Whos aplicable this rate for"
    )
    rate = fields.Monetary(
        string="Rate per hour",
        currency_field="currency_id"
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.EUR'),
        invisible=True
    )
    notes = fields.Text(
        string="Notes",
        help="Notes for the aplicable Rate"
    )
    repair_ids = fields.One2many(
        comodel_name="cwm.repair",
        inverse_name="rate_id",
        string="Associated repairs"
    )
