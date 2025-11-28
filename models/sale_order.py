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
        help='The base price per square meter. Can be overridden in Variants.'
    )
    production_margin = fields.Float(
        string='Production Margin (m)',
        default=0.0,
        help='Extra length to add for production (waste/margins). This will be used in Manufacturing.'
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_price_per_sqm = fields.Float(
        string='Variant Price per Sq/m',
        help='Specific price for this variant. If 0, uses the Template price.'
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

    allow_variable_dimensions = fields.Boolean(
        string='Allow Variable Dimensions',
        default=False,
    )
    price_per_sqm = fields.Float(
        string='Price per Sq/m',
    )

    @api.onchange('product_id')
    def _onchange_product_id_dimensions(self):
        if not self.product_id:
            return

        # Check if the product allows dimensions (from template)
        if self.product_id.product_tmpl_id.allow_variable_dimensions:
            self.allow_variable_dimensions = True
            
            # Fetch prices
            variant_price = self.product_id.variant_price_per_sqm
            template_price = self.product_id.product_tmpl_id.price_per_sqm
            
            # PRIORITY 1: Check if this specific variant has a price set
            if variant_price > 0:
                self.price_per_sqm = variant_price
            # PRIORITY 2: Fallback to the template price
            else:
                self.price_per_sqm = template_price
            
            # Set default dimensions for new lines if not set
            if not self.x_length:
                self.x_length = 1.0
            if not self.x_width:
                self.x_width = 1.0
        else:
            self.allow_variable_dimensions = False
            self.price_per_sqm = 0.0
            self.x_length = 0.0
            self.x_width = 0.0
        
        # Recalculate the final unit price
        self._onchange_dimensions_price()

    @api.onchange('x_length', 'x_width', 'price_per_sqm')
    def _onchange_dimensions_price(self):
        if self.product_id and not self.product_id.product_tmpl_id.allow_variable_dimensions:
            self.x_length = 0.0
            self.x_width = 0.0
            self.price_per_sqm = 0.0

        if self.allow_variable_dimensions and self.price_per_sqm > 0:
            self.price_unit = self.x_length * self.x_width * self.price_per_sqm
        elif not self.allow_variable_dimensions:
            # For standard products, the price is set by the main product_id onchange.
            # We don't need to do anything here to keep the standard price.
            pass

    def _prepare_invoice_line(self, **optional_values):
        """
        Override to pass dimensional fields to the invoice line.
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        if self.allow_variable_dimensions:
            res.update({
                'x_length': self.x_length,
                'x_width': self.x_width,
                'price_per_sqm': self.price_per_sqm,
                'allow_variable_dimensions': self.allow_variable_dimensions,
            })
        else:
            res.update({
                'x_length': 0.0,
                'x_width': 0.0,
                'price_per_sqm': 0.0,
                'allow_variable_dimensions': False,
            })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('product_id'):
                product = self.env['product.product'].browse(vals['product_id'])
                if product.product_tmpl_id.allow_variable_dimensions:
                    # Force fetch variant price on create
                    price = product.variant_price_per_sqm or product.product_tmpl_id.price_per_sqm
                    if price > 0:
                        vals['price_per_sqm'] = price
                        # Recalculate unit price if dimensions are present
                        length = vals.get('x_length', 1.0)
                        width = vals.get('x_width', 1.0)
                        vals['price_unit'] = length * width * price
                        vals['allow_variable_dimensions'] = True

        return super(SaleOrderLine, self).create(vals_list)

    def write(self, vals):
        # If product is changed, ensure we fetch the new price
        if 'product_id' in vals:
            product = self.env['product.product'].browse(vals['product_id'])
            if product.product_tmpl_id.allow_variable_dimensions:
                price = product.variant_price_per_sqm or product.product_tmpl_id.price_per_sqm
                if price > 0:
                    vals['price_per_sqm'] = price
                    # We need to recalculate unit price, but we need current dimensions if not in vals
                    length = vals.get('x_length', self.x_length)
                    width = vals.get('x_width', self.x_width)
                    vals['price_unit'] = length * width * price
        
        return super(SaleOrderLine, self).write(vals)

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