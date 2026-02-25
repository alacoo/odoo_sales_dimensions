from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_print_stock_link = fields.Boolean(
        string='ربط الطباعة بالمخزون',
        config_parameter='ala_dimensions.enable_stock_link',
        default=True,
        help='خصم تلقائي من المخزون عند إكمال مهمة طباعة أو تسجيل هدر. '
             'أوقفه مؤقتاً أثناء الجرد أو تصحيح بيانات المخزون يدوياً.'
    )
