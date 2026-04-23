# -*- coding: utf-8 -*-

{
    'name': 'PoS Discount by Schedule',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Apply automatic discounts at the POS based on configurable schedules',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_discount_rule_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount_by_schedule/static/src/js/pos_store_patch.js',
            'pos_discount_by_schedule/static/src/js/order_model_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
    
