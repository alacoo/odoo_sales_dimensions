from odoo.tests.common import TransactionCase

class TestSaleOrderDimensions(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product_dimensional = self.env['product.template'].create({
            'name': 'Dimensional Product',
            'allow_variable_dimensions': True,
            'price_per_sqm': 50.0,
        })
        self.product_normal = self.env['product.template'].create({
            'name': 'Normal Product',
            'list_price': 100.0,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })

    def test_price_calculation_with_default_sqm_price(self):
        """Test price_unit is calculated with the default price_per_sqm from the product."""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })
        
        sol = self.env['sale.order.line'].new({
            'order_id': sale_order.id,
            'product_id': self.product_dimensional.product_variant_id.id,
        })
        sol._onchange_product_id_dimensions()

        # Check if default price_per_sqm is set correctly
        self.assertEqual(sol.price_per_sqm, 50.0)

        sol.x_length = 2.0
        sol.x_width = 3.0
        sol._onchange_dimensions_price()

        expected_price_unit = 2.0 * 3.0 * 50.0
        self.assertAlmostEqual(sol.price_unit, expected_price_unit)

    def test_price_calculation_with_overridden_sqm_price(self):
        """Test price_unit is calculated with a manually overridden price_per_sqm on the SO line."""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })
        
        sol = self.env['sale.order.line'].new({
            'order_id': sale_order.id,
            'product_id': self.product_dimensional.product_variant_id.id,
        })
        sol._onchange_product_id_dimensions()

        sol.x_length = 2.0
        sol.x_width = 3.0
        # Override the price per sqm on the line
        sol.price_per_sqm = 60.0
        sol._onchange_dimensions_price()

        expected_price_unit = 2.0 * 3.0 * 60.0 # Use the overridden price
        self.assertAlmostEqual(sol.price_unit, expected_price_unit)

    def test_dimensions_for_normal_product(self):
        """Test that dimension fields are zero for a normal product."""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

        sol = self.env['sale.order.line'].new({
            'order_id': sale_order.id,
            'product_id': self.product_normal.product_variant_id.id,
        })
        sol._onchange_product_id_dimensions()

        self.assertEqual(sol.x_length, 0.0)
        self.assertEqual(sol.x_width, 0.0)
        self.assertEqual(sol.price_per_sqm, 0.0)

