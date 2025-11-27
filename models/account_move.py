from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # === Dimensional Fields ===
    # These fields mirror the ones on sale.order.line to allow dimensional
    # pricing to work on standalone invoices.

    x_length = fields.Float(
        string='Length',
        default=1.0,
    )
    x_width = fields.Float(
        string='Width',
        default=1.0,
    )
    price_per_sqm = fields.Float(
        string='Price per Sq/m',
    )

    # UI control field, set via onchange.
    allow_variable_dimensions = fields.Boolean(
        string='Allow Variable Dimensions',
        default=False,
    )

    @api.onchange('product_id')
    def _onchange_product_id_dimensions(self):
        """
        Handles standalone invoices.
        If the line is linked to a sale line, values are populated from it, so we exit early.
        """
        if self.sale_line_ids:
            return

        if self.product_id and self.product_id.product_tmpl_id.allow_variable_dimensions:
            self.allow_variable_dimensions = True
            self.price_per_sqm = self.product_id.product_tmpl_id.price_per_sqm
            if not self.id:
                self.x_length = 1.0
                self.x_width = 1.0
        else:
            self.allow_variable_dimensions = False
            self.price_per_sqm = 0.0
            self.x_length = 0.0
            self.x_width = 0.0
        
        self._onchange_dimensions_price()

    @api.onchange('x_length', 'x_width', 'price_per_sqm')
    def _onchange_dimensions_price(self):
        """
        Calculates the price_unit based on dimensions.
        Also contains a robustness check to reset values if a user tries to enter
        dimensions for a non-dimensional product on a standalone invoice.
        """
        # Do not run this logic for lines created from a Sales Order.
        if self.sale_line_ids:
            return

        if self.product_id and not self.product_id.product_tmpl_id.allow_variable_dimensions:
            self.x_length = 0.0
            self.x_width = 0.0
            self.price_per_sqm = 0.0

        if self.allow_variable_dimensions and self.price_per_sqm > 0:
            self.price_unit = self.x_length * self.x_width * self.price_per_sqm
        elif not self.allow_variable_dimensions:
            # For standard products, the price is set by the main product_id onchange.
            pass