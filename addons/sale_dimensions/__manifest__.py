{
    'name': 'Sale Dimensions',
    'version': '18.0.3.0.0',
    'category': 'Sales',
    'summary': 'إضافة أبعاد الطول والعرض مع حساب السعر بناءً على المساحة',
    'description': '''
## Comprehensive Dimensional Pricing

This addon enhances Odoo's sales process for products sold by area.

**For Users:**
- Activate "Allow Variable Dimensions" on a product.
- Set a "Price per Sq/m" for that product.
- In the Sales Order, when you add this product, you can specify Length and Width.
- The Unit Price will be automatically calculated (Length x Width x Price per Sq/m).
- The Quantity field remains available for specifying the number of copies.
- You can also override the "Price per Sq/m" on any sales order line for flexibility.

**For Developers:**
- The logic is primarily handled via onchange methods on `sale.order.line`.
- `_onchange_product_id_dimensions()`: Sets defaults and a UI control flag.
- `_onchange_dimensions_price()`: Calculates the `price_unit` and enforces dimension rules.
- The UI uses modern Odoo 18 direct attributes (`readonly`, `invisible`) instead of the deprecated `attrs` system.

---

### الوصف بالعربية:

هذه الإضافة تقوم بتطوير أوامر البيع لإدارة المنتجات التي تباع حسب الأبعاد (مثل خدمات الطباعة).

**الميزات الرئيسية:**
- إضافة حقل "سعر المتر المربع" في صفحة المنتج.
- في أمر البيع، يتم حساب "سعر الوحدة" تلقائياً بناءً على الطول والعرض وسعر المتر المربع.
- يبقى حقل "الكمية" متاحاً لإدخال عدد النسخ.
- إمكانية تعديل سعر المتر المربع يدوياً في كل سطر من سطور أمر البيع.
    ''',
    'author': 'Tu Nombre',
    'website': 'https://www.tuempresa.com',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/sale_order_portal_templates.xml',
        'views/reports/sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}