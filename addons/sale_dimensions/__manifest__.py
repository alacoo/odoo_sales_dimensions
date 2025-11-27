{
    'name': 'Sale & Invoice Dimensions',
    'version': '18.0.4.0.0',
    'category': 'Sales/Invoicing',
    'summary': 'Adds dimensional pricing (Length x Width) to Sales and Invoices.',
    'description': '''
## Comprehensive Dimensional Pricing for Sales & Invoicing

This addon enhances Odoo's sales and invoicing process for products sold by area.

**Key Features:**
- **Dimensional Products:** Activate dimensional calculations on a per-product basis.
- **Price by Area:** Set a "Price per Sq/m" on the product.
- **Automatic Price Calculation:** In Sales Orders and Invoices, the Unit Price is automatically calculated from `Length x Width x Price/Sqm`.
- **Manual Quantity:** The `Quantity` field remains independent for entering the number of copies.
- **Flexible Pricing:** The `Price per Sq/m` is editable on each sales/invoice line.
- **SO to Invoice Flow:** Dimensional data is correctly transferred when creating an invoice from a sales order.

---

### الوصف بالعربية:

هذه الإضافة تقوم بتطوير أوامر البيع والفواتير لإدارة المنتجات التي تباع حسب الأبعاد.

**الميزات الرئيسية:**
- إضافة حقل "سعر المتر المربع" في صفحة المنتج.
- في أوامر البيع والفواتير، يتم حساب "سعر الوحدة" تلقائياً بناءً على الطول والعرض وسعر المتر المربع.
- يبقى حقل "الكمية" متاحاً لإدخال عدد النسخ.
- إمكانية تعديل سعر المتر المربع يدوياً في كل سطر.
- نقل بيانات الأبعاد تلقائياً عند إنشاء فاتورة من أمر بيع.
    ''',
    'author': 'Tu Nombre',
    'website': 'https://www.tuempresa.com',
    'depends': ['sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/sale_order_portal_templates.xml',
        'views/reports/sale_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}