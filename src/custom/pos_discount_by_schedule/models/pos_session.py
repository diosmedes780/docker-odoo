# -*- coding: utf-8 -*-

from odoo import models, fields


class PosSession(models.Model):
    _inherit = 'pos.session'
    
    
    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if 'pos.discount.rule' not in result:
            result.append('pos.discount.rule')
        return result
        
    def _loader_params_pos_discount_rule(self):
        return {
            'search_params': {
                'domain': [('active', '=', True)],
                'fields': [
                    'name', 
                    'hour_from', 
                    'hour_to', 
                    'is_exclusive', 
                    'discount_percentage'
                ], 
            },
        }

    def _get_pos_ui_pos_discount_rule(self, params):
        return self.env['pos.discount.rule'].search_read(**params['search_params'])
