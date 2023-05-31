# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CwmCustomer(models.Model):
    _inherit = "res.partner"

    nombre = fields.Char(
        string="PRUEBA"
    )
    function = fields.Char(
        invisible=True
    )
    cars_ids = fields.One2many(
        comodel_name="cwm.car",
        inverse_name="owner",
        string="Cars"
    )

#TODO -Implementación del campo One2many cars