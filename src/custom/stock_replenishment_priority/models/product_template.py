# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    replenishment_priority = fields.Selection(
        [('low', 'Low'), 
        ('average', 'Average'), 
        ('high', 'High')], string="Replenishment priority")
    stock_target = fields.Float(string="Target Stock", help="Desired quantity in stock")

    @api.model
    def run_check_low_stock_activity(self):
        # Buscamos productos que tengan stock_target definido
        products =  self.search([('stock_target', '>', 0)])
        activity_type = self.env.ref('mail.mail_activity_data_todo')
        
        for product in products:
            # We compare available stock vs. target and check for any open activity.
            # If there is any open activity, you will be notified.
            if product.qty_available < product.stock_target:
                # We get the product owner (or we use admin if it's None)
                responsible = product.responsible_id or self.env.ref('base.user_admin')
                
                existing_activity = self.env['mail.activity'].search([
                    ('res_model', '=', 'product.template'),
                    ('res_id', '=', product.id),
                    ('user_id', '=', responsible.id),
                    ('activity_type_id', '=', activity_type.id)
                ])
                
                if not existing_activity:
                        self.env['mail.activity'].create({
                            'res_model_id': self.env['ir.model']._get('product.template').id,
                            'res_id': product.id,
                            'activity_type_id': activity_type.id,
                            'summary': 'Alerta: Stock bajo el objetivo',
                            'note': f'El producto {product.name} tiene {product.qty_available} unidades. El objetivo es {product.stock_target}.',
                            'user_id': responsible.id,
                        })
