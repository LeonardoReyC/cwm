# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CwmWorkers(models.Model):
    _inherit = "hr_employee"



class Workers(models.Model):
    _name = 'cwm.workers'
    _description = 'Workers of the workshop'

    name = fields.Char(
        string="name",
        required=True,
        help="Name of the employee"
    )
    address = fields.Char(
        string="Address",
        reuired=True,
        help="Addres of the worker"
    )
    journey = fields.Integer(
        string="Journey",
        required=True,
        help="How many hours the make the worker"
    )
    salary = fields.Float(
        string="Salary",
        required=True,
        help="How much the worker earn"
    )
    profit = fields.Float(
        string="profits",
        compute="_profits"
    )
    repair_ids = fields.Many2many(
        comodel_name='cwm.repair',
        string='Repairs'
    )

#TODO No hay vistas ni está en el manifes

# TODO-Implementación campo repairs

# TODO-Desarrollar función para calcular los beneficios en bas e la jornada y los trabajos realizados
    @api.depends('journey','max_cap')
    def _profits(self):
        for rec in self:
            rec.profit= int(rec.max_cap)-int(len(rec.animal_ids))
