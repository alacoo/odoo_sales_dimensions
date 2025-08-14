from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    x_length = fields.Float(
        string='Length',
        help='Unit of measure for length, specified in "Unidad de longitud".'
    )
    x_width = fields.Float(
        string='Width',
        help='Unit of measure for width, specified in "Unidad de longitud".'
    )
    x_height = fields.Float(
        string='Height',
        help='Unit of measure for height, specified in "Unidad de longitud".'
    )

    uom_length = fields.Many2one(
        'uom.uom',
        string='Unidad de longitud',
        domain="[('category_id.name', '=', 'Length')]",
        help='Unit of measure for length.'
    )

    def _calculate_product_qty(self, x_length, x_width, x_height):
        return x_length * x_width * x_height

    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(SaleOrderLine, self)._onchange_product_id()

        if self.x_length or self.x_width or self.x_height:
            self._onchange_dimensions()
        
        return res
        
        
    @api.onchange('x_length', 'x_width', 'x_height')
    def _onchange_dimensions(self):
                # Calcular la cantidad
        if self.x_length > 0 and self.x_width > 0 and self.x_height > 0:
            self.product_uom_qty = self._calculate_product_qty(
                self.x_length, self.x_width, self.x_height
            )
        else:
            self.product_uom_qty = 0.0
            
        if not self.product_id:
            return
        # Lógica para manejar valores inválidos y notificar
        for field_name in ['x_length', 'x_width', 'x_height']:
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

        # Calcular la cantidad
        if self.x_length > 0 and self.x_width > 0 and self.x_height > 0:
            self.product_uom_qty = self._calculate_product_qty(
                self.x_length, self.x_width, self.x_height
            )
        else:
            self.product_uom_qty = 0.0

        # Lógica para mostrar la advertencia si todas las dimensiones son cero
        if self.x_length == 0.0 and self.x_width == 0.0 and self.x_height == 0.0:
            return {
                'warning': {
                    'title': 'Dimensions Error',
                    'message': 'All dimensions are 0. The quantity and subtotal for this line will be 0.',
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'x_length' in vals and 'x_width' in vals and 'x_height' in vals:
                vals['product_uom_qty'] = self._calculate_product_qty(vals['x_length'], vals['x_width'], vals['x_height'])
        return super(SaleOrderLine, self).create(vals_list)

    def write(self, vals):
        if any(f in vals for f in ['x_length', 'x_width', 'x_height']):

            res = super(SaleOrderLine, self).write(vals)
            for line in self:
                line.product_uom_qty = line._calculate_product_qty(line.x_length, line.x_width, line.x_height)
            return res
        return super(SaleOrderLine, self).write(vals)
    



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_line_dimensions = fields.Char(
        string="Dimensions",
        compute='_compute_line_dimensions',
        store=True
    )

    @api.depends('order_line.x_length', 'order_line.x_width', 'order_line.x_height')
    def _compute_line_dimensions(self):
        for order in self:
            dimensions_list = []
            for line in order.order_line:
                if line.x_length or line.x_width or line.x_height:
                    dims = f"L: {line.x_length}, W: {line.x_width}, H: {line.x_height}"
                    dimensions_list.append(dims)
            order.x_line_dimensions = "; ".join(dimensions_list)