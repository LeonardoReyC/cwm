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
        string="Vin Num",
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
    repair_ids = fields.One2many(
        comodel_name="cwm.repair",
        inverse_name="car_id",
        string="Repairs"
    )
    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="cwm.car.stage",
        group_expand='_read_group_stage_ids',
    )
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_obj = self.env['cwm.car.stage']
        folded_stages = stage_obj.search([('fold', '=', False)])
        return folded_stages
