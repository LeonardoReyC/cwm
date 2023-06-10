# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields
from odoo import api


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
