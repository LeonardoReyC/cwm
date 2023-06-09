# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields
from odoo import api
from odoo import _
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
    vehicle_id = fields.Many2one(
        comodel_name='cwm.car',
        string="Vehicle",
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
    time_spent = fields.Float(
        string="Total Time spent",
        compute="_compute_spent_time",
    )
    profit = fields.Monetary(
        string="Profit",
        compute="_compute_profit",
        currency_field="currency_id",
    )
    color = fields.Integer(
        string="color",
        compute="_compute_color",
    )
    stage_id = fields.Many2one(
        string="Stage",
        comodel_name="cwm.repair.stage",
        group_expand='_read_group_stage_ids',
    )
    start_date = fields.Datetime(
        string="Start date",
        help="Moment when the repair starts"
    )
    end_date = fields.Datetime(
        string="End date",
        help="Moment when the repair is finished"
    )

    # Automatic end stage set once end date has set
    @api.constrains('end_date')
    def repair_completed(self):
        for rec in self:
            if rec.end_date:
                rec.stage_id = self.env['cwm.repair.stage'].search([('sequence', '=', '14')], limit=1)

    # Unfold stages return
    @api.model
    def _read_group_stage_ids(self,groups, domain, order):
        stage_obj = self.env['cwm.repair.stage']
        unfolded_stages = stage_obj.search([('fold', '=', False)])
        return unfolded_stages

    # Set color ribbon on kanban based on the difference between the budget and profit fields
    @api.constrains('profit', 'budget')
    def _compute_color(self):
        low = self.env['cwm.repair.indicator'].search([('name', '=', 'Low')])
        medium = self.env['cwm.repair.indicator'].search([('name', '=', 'Medium')])
        ok = self.env['cwm.repair.indicator'].search([('name', '=', 'OK')])
        for rec in self:
            if rec.profit < 0 or rec.budget < 0:
                rec.color = 9
                continue
            control = (rec.profit * 100) / rec.budget
            if control >= 0 and control < low.limit:
                rec.color = low.assigned_color
            elif control >= low.limit and control < medium.limit:
                rec.color = medium.assigned_color
            else:
                rec.color = ok.assigned_color

    # Profit calculation
    @api.depends('time_spent', 'allotted_time')
    def _compute_profit(self):
        for rep in self:
            rep.profit = 0.0
            rep.profit = rep.budget
            for task in rep.task_ids:
                rep.profit -= task.cost

    # Automatic change of stage based on time consumed
    @api.onchange('time_spent', 'allotted_time')
    def _onchange_time_spent_allotted_time(self):
        for rec in self:
            if self.time_spent <= 0:
                repair_stage = self.env['cwm.repair.stage'].search([('sequence', '=', '10')], limit=1)
                self.stage_id = repair_stage
            elif 0 < self.time_spent < self.allotted_time:
                repair_stage = self.env['cwm.repair.stage'].search([('sequence', '=', '11')], limit=1)
                self.stage_id = repair_stage
                car_stage = self.env['cwm.car.stage'].search([('sequence', '=', '11')], limit=1)
                self.vehicle_id.stage_id = car_stage
            elif self.time_spent > self.allotted_time:
                repair_stage = self.env['cwm.repair.stage'].search([('sequence', '=', '13')], limit=1)
                self.stage_id = repair_stage

    # Calculation of total time spent based on tasks performed and assignment
    # of start date based on first task performed
    @api.depends('time_spent', 'allotted_time', 'task_ids')
    def _compute_spent_time(self):
        for rep in self:
            rep.time_spent = 0.0
            for task in rep.task_ids:
                if not rep.start_date:
                    rep.start_date = fields.Datetime.now()
                rep.time_spent += task.time_spent

    # Calculation of the budget allocated based on time and rate
    @api.depends('budget', 'allotted_time')
    def _compute_budget(self):
        for rec in self:
            rec.budget = (rec.rate_id.rate * rec.allotted_time)

    # Sequence number generation at repair creation
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
        string="Time Spent",
        required=True,
        help="Time spent on the operation"
    )
    repair_id = fields.Many2one(
        comodel_name='cwm.repair',
        required=True,
        string='Repair',
    )
    worker_id = fields.Many2one(
        comodel_name='hr.employee',
        required=True,
        string='Worker',
    )
    cost = fields.Monetary(
        string="Cost",
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.EUR')
    )

    # Calculation of the cost of performing the task based on the employee's salary.
    @api.constrains('time_spent')
    def calculate_cost(self):
        for rec in self:
            rec.cost = (rec.worker_id.salary_hour * rec.time_spent)
