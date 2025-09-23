from odoo.tests.common import TransactionCase

class TestSaleOrderDimensions(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Producto Test',
            'type': 'consu',
            'list_price': 10.0,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Cliente Test',
        })

    def test_sale_order_line_dimensions(self):
        print(" ")
        print(">>> Iniciando test_sale_order_line_dimensions")
        print(" ")

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

        line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product.id,
            'x_length': 2.0,
            'x_width': 3.0,
            'price_unit': self.product.list_price,
        })

        expected_qty = 2.0 * 3.0
        expected_subtotal = expected_qty * line.price_unit  

        print(f"Length: {line.x_length}")
        print(f"Width: {line.x_width}")
        print(f"Quantity calculated: {line.product_uom_qty}")
        print(f"Quantity expected: {expected_qty}")
        print(f"Subtotal calculated: {line.price_subtotal}")
        print(f"Subtotal expected: {expected_subtotal}")
        
        self.assertEqual(line.product_uom_qty, expected_qty, "La cantidad calculada no coincide con las dimensiones.")

        self.assertEqual(line.price_subtotal, expected_subtotal, "El subtotal del pedido no coincide con el cálculo esperado.")
        print(" ")
        print(">>> Test completado.")
        print(" ")

