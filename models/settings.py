# -*- coding: utf-8 -*-


from odoo import models
from odoo import fields
from odoo import api
from odoo import _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


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

class CwmSequence(models.Model):
    _name = 'cwm.sequence'
    _description = 'Sequence'

    def get_sequence(self, seq_name):
        seq = self.env['cwm.sequence'].search([('name', '=', seq_name)])
        if not seq:
            raise UserError(_("Sequence %s not found.") % seq_name)
        if str(seq.suffix) != str(fields.Date.today().year):
            seq.suffix = str(fields.Date.today().year)
            seq.actual_value = 0
            seq.next_value = 0

        sequence = seq.prefix + "-" + str(str(seq.next_value).rjust(5, '0')) + " /" + seq.suffix
        seq.actual_value = seq.next_value
        seq.next_value += 1
        seq.write({'next_value': seq.next_value, 'actual_value': seq.actual_value})
        return sequence

    name = fields.Char(
        string="Seq Name",
        required=True,
        help="Sequence name"
    )
    prefix = fields.Char(
        string="Prefix",
        required=True,
        help="Prefix of the sequence"
    )
    suffix = fields.Char(
        string="Sufix",
        help="Suffix set the actual year"
    )
    actual_value = fields.Integer(
        string="Actual Value",
        help="The last number used"
    )
    next_value = fields.Integer(
        string="Next Value",
        help="The Next value"
    )


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

    @api.onchange('name')
    def onchange_car_brand(self):
        if self.name:
            self.name = self.name.capitalize()


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

    @api.onchange('name')
    def onchange_car_model(self):
        if self.name:
            self.name = self.name.capitalize()


class CarRepairsProfitIndicator(models.Model):
    _name = "cwm.repair.indicator"
    _description = "Repair profits kanban view indicator"

    name = fields.Char(
        string="Level Indicator",
        help="Indicator for repair kanban view color",
        readonly=True
    )
    limit = fields.Integer(
        string="Percentage level",
        help="An integer number representing % "
    )
    assigned_color = fields.Integer(
        string="Color indicator",
        help="An integer number representing a color"
    )
    notes = fields.Text(
        string="Notes",
        help="Indication notes"
    )


class CwmCarStage(models.Model):
    _name = 'cwm.car.stage'
    _description = 'Car Stage'
    _order = 'sequence, id'

    sequence = fields.Integer(
        default=50
    )
    name = fields.Char(
        required=True,
        translate=True
    )
    fold = fields.Boolean(
        string='Folded in Kanban',
        help="If enabled, this stage will be displayed as folded in the Kanban view of your projects. "
             "Projects in a folded stage are considered as closed."
    )


class CwmCarStage(models.Model):
    _name = 'cwm.repair.stage'
    _description = 'Repair Stage'
    _order = 'sequence, id'

    sequence = fields.Integer(
        default=50
    )
    name = fields.Char(
        required=True,
        translate=True
    )
    fold = fields.Boolean(
        string='Folded in Kanban',
        help="If enabled, this stage will be displayed as folded in the Kanban view of your projects. "
             "Projects in a folded stage are considered as closed."
    )

class CwmCarStage(models.Model):
    _name = 'cwm.color'
    _description = 'Description color'

    name = fields.Char(
        string="color name",
        required=True,
        inverse='_inverse_general_color'
    )
    enable = fields.Boolean(
        string="Enabled color",
    )

    def _inverse_general_color(self):
        if self.name:
            self.name = self.name.capitalize()

    @api.onchange('name')
    def onchange_general_color(self):
        if self.name:
            self.name = self.name.capitalize()
