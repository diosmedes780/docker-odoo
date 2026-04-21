# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    replenishment_priority = fields.Selection(
        [('low', 'Low'), 
        ('average', 'Average'), 
        ('high', 'High')], string="Replenishment priority")
    stock_target = fields.Float(string="Target Stock", help="Desired quantity in stock")
