# -*- coding: utf-8 -*-

# TODO odoo.odoo
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
    time_spent = fields.Float(
        string="Total Time spent",
        compute="_compute_spent_time",
    )
    status = fields.Selection(
        [('1', 'Pending start'),
         ('2', 'Started'),
         ('3', 'Stopped'),
         ('4', 'Time exceeded'),
         ('5', 'Completed')],
        string="Repair status",
        group_expand='_expand_states',
        default='1',
        index=True,
        required=True
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

    @api.constrains('profit', 'budget')
    def _compute_color(self):
        for rec in self:
            if rec.profit < 0 or rec.budget < 0:
                rec.color = 9
                continue
            control = (rec.profit * 100)/ rec.budget
            if control >= 0 and control < 20:
                rec.color = 1
            elif control >= 20 and control < 60:
                rec.color = 3
            else:
                rec.color = 10

    def _expand_states(self, state, domain, order):
        return [key for key, val in type(self).status.selection]

    @api.depends('time_spent', 'allotted_time')
    def _compute_profit(self):
        for rep in self:
            rep.profit = 0.0
            rep.profit = rep.budget
            for task in rep.task_ids:
                rep.profit -= task.cost

    @api.onchange('time_spent', 'allotted_time', 'status')
    def _onchange_time_spent_allotted_time(self):
        if self.time_spent <= 0:
            self.status = '1'  # Pending start
        elif 0 < self.time_spent < self.allotted_time:
            self.status = '2'  # Started
            self.car_id.state = '2'
        elif self.time_spent > self.allotted_time:
            self.status = '4'  # Completed

    @api.depends('time_spent', 'allotted_time', 'task_ids')
    def _compute_spent_time(self):
        for rep in self:
            rep.time_spent = 0.0
            for task in rep.task_ids:
                rep.time_spent += task.time_spent

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

    @api.constrains('time_spent')
    def calculate_cost(self):
        for rec in self:
            rec.cost = (rec.worker_id.salary_hour * rec.time_spent)
