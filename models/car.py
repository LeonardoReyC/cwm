# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CwmCars(models.Model):
    _name = 'cwm.car'
    _description = 'Cars'
    _rec_name = "plate_number"

    id = fields.Integer(

    )

    plate_number = fields.Char(
        string="Plate Number",
        required=True,
        unique=True,
        help="Plate vehicle number"
    )
    picture = fields.Image(
        string="Image",
    )
    vin_number = fields.Char(
        string="Vin Number",
        required=True,
        unique=True,
        help="Unique vehícle number"
    )
    brand_id = fields.Many2one(
        comodel_name="cwm.car.brand",
        string="Brand",
        store=True
    )
    model_id = fields.Many2one(
        comodel_name="cwm.car.model",
        string="Model"
    )
    owner = fields.Many2one(
        comodel_name="res.partner",
        string="Owner"
    )
    state = fields.Selection(
        [('1', 'Pending appointment'),
        ('2', 'Under repair'),
        ('3', 'Waiting for spare parts'),
        ('4', 'Repaired'),
        ('5', 'Delivered')],
        required=True
    )
    repair_ids = fields.One2many(
        comodel_name="cwm.repair",
        inverse_name="car_id",
        string="Repairs"
    )
    def _compute_xml_id(self):
        res= self.get_external_

#TODO One2many repairs
