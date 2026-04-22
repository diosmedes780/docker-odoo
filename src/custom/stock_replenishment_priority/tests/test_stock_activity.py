# -*- coding: utf-8 -*-
print("--- CARGANDO EL ARCHIVO DE TESTS ---")
from odoo.tests import common, tagged


@tagged('post_install', '-at_install')
class TestStockActivity(common.TransactionCase):
    
    def setUp(self):
        super(TestStockActivity, self).setUp()
        # We created a user to test the assignment of 'responsible_id'
        self.test_user = self.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'resp_test'
        })
        
        # We created the test product
        self.product = self.env['product.template'].create({
            'name': 'Test product',
            'stock_target': 100.0,
            'qty_available': 10.0,
            'responsible_id': self.test_user.id
        })
    
    def test_run_check_low_stock_activity_creates_activity(self):
        """Enable the creation of an activity if stock is low."""
        self.env['product.template'].run_check_low_stock_activity()
        
        activity = self.env['mail.activity'].search([
            ('res_id', '=', self.product.id),
            ('res_model', '=', 'product.template'),
            ('user_id', '=', self.test_user.id)
        ])
        
        self.assertEqual(len(activity), 1, "Exactly one activity should have been created.")
        self.assertEqual(activity.summary, 'Alerta: Stock bajo el objetivo')

    def test_prevent_duplicate_activity(self):
        
        self.env['product.template'].run_check_low_stock_activity()
        self.env['product.template'].run_check_low_stock_activity()
        
        activities = self.env['mail.activity'].search([
            ('res_id', '=', self.product.id),
            ('res_model', '=', 'product.template'),
            ('user_id', '=', self.test_user.id)
        ])
        
        self.assertEqual(len(activities), 1, "A second activity should not be created if one already exists.")
