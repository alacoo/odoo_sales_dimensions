from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    allow_variable_dimensions = fields.Boolean(
        string='السماح ببيع المنتج هذا بحسب المتغيرات (الطول والعرض)',
        help='If checked, you can sell this product with variable length and width on the sales order.'
    )
