# -*- coding: utf-8 -*-

from odoo import models
from odoo import fields
from odoo import api


class CwmWorkers(models.Model):
    _inherit = "hr.employee"

    task_ids = fields.One2many(
        comodel_name="cwm.repair.task",
        inverse_name="worker_id",
        string="Worker Associated"
    )
    salary_hour = fields.Monetary(
        string="Salary per hour",
        required=True,
        help="How much is charger per 1 hour",
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.ref('base.EUR')
    )

