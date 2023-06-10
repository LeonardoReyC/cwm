from odoo import models
from odoo import fields
from odoo import api
import requests


# API PROVIDER: NHTSA web: https://vpic.nhtsa.dot.gov/api/

class CwmCarsApi(models.TransientModel):
    _name = 'cwm.cars.api'
    _description = 'api'

    name = fields.Char(
        string="Brand"
    )
    model = fields.Char(
        string="Model"
    )

    # Extraction models and brands from api into brand and models models
    def consult_brands(self, brand):
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/" + brand + "?format=json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        results = data.get('Results', [])
        for result in results:
            brand = result.get('Make_Name')
            model = result.get('Model_Name')

            brand_record = self.env['cwm.car.brand'].search([('name', '=', brand)], limit=1)
            if not brand_record:
                brand_record = self.env['cwm.car.brand'].create({'name': brand})

            if model and not self.env['cwm.car.model'].search(
                    [('name', '=', model), ('brand_id', '=', brand_record.id)]):
                self.env['cwm.car.model'].create({'name': model, 'brand_id': brand_record.id})

    # Getting all database from models and brands into transient model
    def consult_transient(self):
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/*?format=json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        results = data.get('Results', [])
        for result in results:
            self.env['cwm.cars.api'].sudo().create({
                'name': result.get('Make_Name'),
                'model': result.get('Model_Name'),
            })
