# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CarWorkshopManager(models.Model):
    _name = 'cwm.cwm'
    _description = 'cwm.cwm'

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the workshop"
    )
    address = fields.Char(
        string="address",
        required=True,
        help="Workshop Address"
    )


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
