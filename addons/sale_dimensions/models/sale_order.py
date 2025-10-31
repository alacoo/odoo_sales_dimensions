from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    allow_variable_dimensions = fields.Boolean(
        string='Allow Variable Dimensions',
        help='Enable this to allow specifying length and width on sale order lines for this product.'
    )
    price_per_sqm = fields.Float(
        string='Price per Sq/m',
        help='The price per square meter for products sold by dimension.'
    )

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    x_length = fields.Float(
        string='Length',
        default=1.0,
        help='Unit of measure for length, specified in "Unidad de longitud".'
    )
    x_width = fields.Float(
        string='Width',
        default=1.0,
        help='Unit of measure for width, specified in "Unidad de longitud".'
    )

    uom_length = fields.Many2one(
        'uom.uom',
        string='Unidad de longitud',
        domain="[('category_id.name', '=', 'Length')]",
        help='Unit of measure for length.'
    )

    # This is a non-stored field used to control the UI (e.g., readonly attributes).
    # It is set manually in the _onchange_product_id_dimensions method because relying
    # on a related field proved unreliable with the Odoo 18 web client's new view rendering.
    allow_variable_dimensions = fields.Boolean(
        string='Allow Variable Dimensions',
        default=False,
    )
    price_per_sqm = fields.Float(
        string='Price per Sq/m',
    )

    @api.onchange('product_id')
    def _onchange_product_id_dimensions(self):
        """ 
        Triggered when the product is changed on the SO line.
        - Checks if the new product is a dimensional product.
        - Sets the 'allow_variable_dimensions' flag for UI control.
        - Sets the default price_per_sqm from the product.
        - Resets dimension fields to 0 for non-dimensional products.
        """
        if self.product_id and self.product_id.product_tmpl_id.allow_variable_dimensions:
            self.allow_variable_dimensions = True
            self.price_per_sqm = self.product_id.product_tmpl_id.price_per_sqm
            # Only set default dimensions for brand new lines, not when editing existing ones.
            if not self.id:
                self.x_length = 1.0
                self.x_width = 1.0
        else:
            self.allow_variable_dimensions = False
            self.price_per_sqm = 0.0
            self.x_length = 0.0
            self.x_width = 0.0
        
        # Trigger the price calculation after setting the defaults.
        self._onchange_dimensions_price()

    @api.onchange('x_length', 'x_width', 'price_per_sqm')
    def _onchange_dimensions_price(self):
        """
        Triggered when any dimensional value is changed.
        - Calculates the unit price based on dimensions and price_per_sqm.
        - Contains a fallback check to enforce that dimensions are 0 for non-dimensional products.
          This is a robust workaround for potential UI unresponsiveness where a user might
          be able to enter values in a field that should be readonly.
        """
        # Robustness check: If the product is not dimensional, forcibly reset the values.
        if self.product_id and not self.product_id.product_tmpl_id.allow_variable_dimensions:
            self.x_length = 0.0
            self.x_width = 0.0
            self.price_per_sqm = 0.0

        # Main price calculation logic
        if self.allow_variable_dimensions and self.price_per_sqm > 0:
            self.price_unit = self.x_length * self.x_width * self.price_per_sqm
        elif not self.allow_variable_dimensions:
            # For standard products, the price is set by the main product_id onchange in Odoo.
            # We do nothing here to avoid interfering with standard behavior.
            pass

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_line_dimensions = fields.Char(
        string="Dimensions",
        compute='_compute_line_dimensions',
        store=True
    )

    @api.depends('order_line.x_length', 'order_line.x_width', 'order_line.allow_variable_dimensions')
    def _compute_line_dimensions(self):
        for order in self:
            dimensions_list = []
            for line in order.order_line:
                if line.allow_variable_dimensions and (line.x_length or line.x_width):
                    dims = f"L: {line.x_length}, W: {line.x_width}"
                    dimensions_list.append(dims)
            order.x_line_dimensions = "; ".join(dimensions_list)