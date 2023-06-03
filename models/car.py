# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CwmCars(models.Model):
    _name = 'cwm.car'
    _description = 'Cars'
    _rec_name = "plate_number"

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
        string="State",
        default='1',
        group_expand='_expand_states',
        index=True,
        required=True
    )
    repair_ids = fields.One2many(
        comodel_name="cwm.repair",
        inverse_name="car_id",
        string="Repairs"
    )

    def _expand_states(self, state, domain, order):
        return [key for key, val in type(self).state.selection]

#TODO One2many repairs
