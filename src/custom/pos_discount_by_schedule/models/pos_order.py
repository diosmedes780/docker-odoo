# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pytz
from datetime import datetime


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    @api.model
    def _process_order(self, order, draft, existing_order):
        
        # 1. Obtener la hora actual de la orden (en formato hora de 0.0 a 24.0)
        tz = pytz.timezone(self.env.user.tz or 'UTC')
        order_date = datetime.now(tz)
        current_hour = order_date.hour + (order_date.minute / 60.0)
        
        # Obtenemos las líneas de forma segura, accediendo primero a 'data'
        order_data = order.get('data', {})
        lines = order_data.get('lines', [])
        
        # 2. Buscar si existe una regla activa para esta hora
        rule = self.env['pos.discount.rule'].sudo().search([
            ('hour_from', '<=', current_hour),
            ('hour_to', '>', current_hour)
        ], limit=1)
        
        # ~ print(lines, flush=True)
        # 3. Si hay regla, aplicamos el descuento a las líneas
        if rule:
            for line in lines:
                
                # Posición 2 es el diccionario de valores del método _order_fields
                line_data = line[2]
                
                # Caso A: Si la regla es exclusiva, obligamos a aplicar nuestro descuento
                # (ignoramos/sobrescribimos cualquier descuento manual previo)
                if rule.is_exclusive:
                    print("Es exclusiva")
                    line_data['discount'] = rule.discount_percentage    
                
                if not line_data.get('discount'):
                    line_data['discount'] = rule.discount_percentage
                    
        return super(PosOrder, self)._process_order(order, draft, existing_order)    
