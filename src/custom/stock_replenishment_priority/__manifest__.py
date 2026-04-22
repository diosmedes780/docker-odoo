# -*- coding: utf-8 -*-

{
    'name': 'Stock - Product',
    'version': '17.0.1.0.0',
    'category': 'Stock',
    'summary': 'Replenishment rules by priority',
    'depends': ['base','product','stock'],
    'data': [
        'data/ir_cron_data.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
