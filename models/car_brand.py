# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CarBrands(models.Model):
    _name = 'cwm.car.brand'
    _description = 'Brand name for cars'

    name = fields.Char(
        string="Brand name",
        required=True,
        help="Brand car name"
    )
    model_ids = fields.One2many(
        comodel_name="cwm.car.model",
        inverse_name="brand_id",
        string="Model list"
    )

class CarModels(models.Model):
    _name = "cwm.car.model"
    _description = "car models of a brand"

    name = fields.Char(
        string="Model name",
        required=True,
        help="Model name"
    )
    brand_id = fields.Many2one(
        comodel_name="cwm.car.brand",
        string="Brand"
    )


