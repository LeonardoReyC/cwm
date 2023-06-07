# -*- coding: utf-8 -*-
{
    'name': "CWM",

    'summary': """
        Vehicle repair shop management module""",

    'description': """
        This application is designed to manage a small repair shop. 
        It has models for cars, workers, customers, repairs and 
        replacement vehicles. It has different types of views to 
        be able to carry out the management in an effective way.
    """,

    'author': "My Company",
    'website': "https://www.cwm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'project',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_workshop.xml',
        'views/views_car.xml',
        'views/views_customer.xml',
        'views/views_workers.xml',
        'data/data.xml',
        'views/views_repair.xml',
        'views/views_settings.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True
}
