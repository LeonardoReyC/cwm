# -*- coding: utf-8 -*-

#TODO odoo.odoo
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CwmRepair(models.Model):
    _name = 'cwm.repair'
    _rec_name = "rep_num"

    name = fields.Selection(
        [('1', 'Vehicle maintenance'),
         ('2', 'Mechanical repair'),
         ('3', 'Body Repair'),
         ('4', 'Bodywork and mechanical repair')],
        string="Type of operation",
        default='3',
        index=True,
        required=True
    )
    sequence = fields.Many2one(
        comodel_name='cwm.sequence',
        string='Sequence',
        default=lambda self: self.env['cwm.sequence'].search([('name', '=', 'Repairs')], limit=1),
        readonly=True,
        invisible=True,
    )
    rep_num = fields.Char(
        string='OR',
        readonly=True
    )
    car_id = fields.Many2one(
        comodel_name='cwm.car',
        string="Car",
        required=True,
    )
    budget = fields.Monetary(
        string="Budget",
        compute="_compute_budget",
        currency_field="currency_id",
    )
    allotted_time = fields.Float(
        string="Allotted time",
        required=True,
        help="1 unit = 60mins: 0.25 units = 15mins"
    )
    rate_id = fields.Many2one(
        comodel_name='cwm.rates',
        string='Applicable Rate',
        default=lambda self: self.env['cwm.rates'].search([('name', '=', 'General')], limit=1)
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.EUR')
    )
    task_ids = fields.One2many(
        comodel_name="cwm.repair.task",
        inverse_name="repair_id",
        string="Tasks Associated"
    )


    @api.depends('budget', 'allotted_time')
    def _compute_budget(self):
        for rec in self:
            rec.budget = (rec.rate_id.rate * rec.allotted_time)

    @api.model
    def create(self, vals):
        seq_name = 'Repairs'
        sequence = self.env['cwm.sequence'].search([('name', '=', seq_name)], limit=1)
        if not sequence:
            raise UserError(_("Sequence %s not found.") % seq_name)
        vals['rep_num'] = sequence.get_sequence(seq_name)
        vals['sequence'] = sequence.id
        return super(CwmRepair, self).create(vals)


class CwmRepairTasks(models.Model):
    _name = 'cwm.repair.task'

    name = fields.Char(
        string="Operation performed",
        required=True
    )
    time_spent = fields.Float(
        string="Minutes Spent",
        required=True,
        help="Time spent in minutes"
    )
    time_to_compute = fields.Float(
        string="Hour units",
        compute="_compute_hour_units",
    )
    repair_id = fields.Many2one(
        comodel_name='cwm.repair',
        string='Repair',
    )

    @api.depends('time_spent')
    def _compute_hour_units(self):
        for rec in self:
            rec.time_to_compute = (rec.time_spent / 60.00)

    """
    worker_ids = fields.Many2many(
        comodel_name='cwm.workers',
        string='Workers'
    )
    """