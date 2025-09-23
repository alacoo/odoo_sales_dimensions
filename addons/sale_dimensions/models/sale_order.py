from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    allow_variable_dimensions = fields.Boolean(
        related='product_template_id.allow_variable_dimensions',
        string='Allow Variable Dimensions'
    )
    
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

    def _calculate_product_qty(self, x_length, x_width):
        return x_length * x_width

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(SaleOrderLine, self)._onchange_product_id()

        if self.x_length or self.x_width:
            self._onchange_dimensions()
        
        return res
        
        
    @api.onchange('x_length', 'x_width')
    def _onchange_dimensions(self):
        if self.allow_variable_dimensions:
            # Calcular la cantidad
            if self.x_length > 0 and self.x_width > 0:
                self.product_uom_qty = self._calculate_product_qty(
                    self.x_length, self.x_width
                )
            else:
                self.product_uom_qty = 0.0

            if not self.product_id:
                return
            # Lógica para manejar valores inválidos y notificar
            for field_name in ['x_length', 'x_width']:
                value = getattr(self, field_name)
                if not isinstance(value, (int, float)) or value < 0:
                    setattr(self, field_name, 0.0)
                    self.product_uom_qty = 0.0
                    return {
                        'warning': {
                            'title': 'Invalid Dimension Value',
                            'message': f'{field_name.replace("x_", "").capitalize()} must be a non-negative number.',
                        }
                    }

            # Lógica para mostrar la advertencia si todas las dimensiones son cero
            if self.x_length == 0.0 and self.x_width == 0.0:
                return {
                    'warning': {
                        'title': 'Dimensions Error',
                        'message': 'All dimensions are 0. The quantity and subtotal for this line will be 0.',
                    }
                }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_template = self.env['product.template'].search([('id', '=', vals.get('product_template_id'))])
            if product_template.allow_variable_dimensions:
                length = vals.get('x_length', 1.0)
                width = vals.get('x_width', 1.0)
                vals['product_uom_qty'] = self._calculate_product_qty(length, width)
        return super(SaleOrderLine, self).create(vals_list)

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for line in self:
            if line.allow_variable_dimensions:
                if any(f in vals for f in ['x_length', 'x_width']):
                    line.product_uom_qty = line._calculate_product_qty(line.x_length, line.x_width)
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_line_dimensions = fields.Char(
        string="Dimensions",
        compute='_compute_line_dimensions',
        store=True
    )

    @api.depends('order_line.x_length', 'order_line.x_width')
    def _compute_line_dimensions(self):
        for order in self:
            dimensions_list = []
            for line in order.order_line:
                if line.product_id.allow_variable_dimensions and (line.x_length or line.x_width):
                    dims = f"L: {line.x_length}, W: {line.x_width}"
                    dimensions_list.append(dims)
            order.x_line_dimensions = "; ".join(dimensions_list)