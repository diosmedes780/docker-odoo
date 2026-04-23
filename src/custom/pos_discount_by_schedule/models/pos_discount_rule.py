# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosDiscountRule(models.Model):
    _name = 'pos.discount.rule'
    _description = 'Time-Based Discount Rule'
    _rec_name = 'name'
    
    
    name = fields.Char(string="Name", required=True)
    hour_from = fields.Float(
        string="Start Time", 
        rerquired=True, help="Example: 08.00 for 8 AM")
    hour_to = fields.Float(
        string="End Time", 
        required=True, help="Example: 20.00 for 8 PM")
    discount_percentage = fields.Float(string="Discount (%)", required=True)
    is_exclusive = fields.Boolean(
        string="¿Exclusive Discount?", 
        default=False, 
        help="If checked, this discount overrides any other manual discounts on the line.")
    active = fields.Boolean(string="Active", default=True)
    
    @api.constrains('hour_from', 'hour_to', 'active')
    def _check_hours(self):
        for rule in self:
            if rule.hour_from >= rule.hour_to:
                raise ValidationError(_('The start time must be earlier than the end time.'))
            if not (0 <= rule.hour_from <= 24 and 0 <= rule.hour_to <= 24):
                raise ValidationError(_("The hours must be between 0 and 24."))
            
            overlapping_rule = self.search([
                ('id', '!=', rule.id),
                ('active', '=', True),
                ('hour_from', '<', rule.hour_to),
                ('hour_to', '>', rule.hour_from),
            ], limit=1)
            
            if overlapping_rule:
                raise ValidationError(_(
                    f"There is a scheduling conflict with the rule '{overlapping_rule.name}' "
                    f"({overlapping_rule.hour_from} - {overlapping_rule.hour_to}). "
                    f"You cannot have two active rules at the same time."
                ))
    
    @api.constrains('discount_percentage')
    def _check_discount(self):
        for rule in self:
            if not (0 < rule.discount_percentage <= 100):
                raise ValidationError(_("The discount percentage must be between 0 and 100."))
