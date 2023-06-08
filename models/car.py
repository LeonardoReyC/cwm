# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CwmCars(models.Model):
    _name = 'cwm.car'
    _description = 'Cars'
    _rec_name = "plate_number"

    plate_number = fields.Char(
        string="Plate Number",
        required=True,
        unique=True,
        help="Plate vehicle number",
        placeholder="Plate Number"
    )
    brand_id = fields.Many2one(
        comodel_name="cwm.car.brand",
        string="Brand",
        store=True,
        required=True,
    )
    model_id = fields.Many2one(
        comodel_name="cwm.car.model",
        string="Model",
        required=True,
    )
    registration_date = fields.Date(
        string="Registration date",
        required=True,
        help="When the vehicle was registered"
    )
    next_appointment = fields.Date(
        string="Next Appointment",
        help="Date for next appointment"
    )
    entry_date = fields.Date(
        string="Entry Date",
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
    owner = fields.Many2one(
        comodel_name="res.partner",
        string="Owner",
        required=True,
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
    body_color = fields.Many2one(
        string="Car color",
        comodel_name="cwm.color",
    )

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_obj = self.env['cwm.car.stage']
        folded_stages = stage_obj.search([('fold', '=', False)])
        return folded_stages

    @api.onchange('vin_number')
    def onchange_check_vin_number_length(self):
        if self.vin_number:
            if len(self.vin_number) != 17:
                raise ValidationError('Vin number must be 17 characters.')
            self.vin_number = self.vin_number.upper()

    @api.onchange('plate_number', 'brand_id')
    def onchange_plate_number(self):
        if self.plate_number:
            self.plate_number = self.plate_number.upper()

"""
    @api.constrains('vin_number')
    def _check_vin_number_length(self):
        for rec in self:
            if len(rec.vin_number) != 17:
                raise ValidationError('Vin number must be 17 characters.')
"""
