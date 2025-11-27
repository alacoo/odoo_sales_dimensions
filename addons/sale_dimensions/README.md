# Sale & Invoice Dimensions Addon

This document is also available in Arabic below.

---

## 1. Purpose

This addon extends the functionality of Odoo Sales and Invoicing applications to allow selling products based on dimensions (length and width), with the price calculated based on the area. It is specifically designed for businesses that sell services like printing, where the price depends on the surface area of the job, and where multiple copies of the same dimensional item might be ordered.

The core logic changes the **Unit Price** of the order/invoice line based on the dimensions, while the **Quantity** field remains available for the user to specify the number of copies.

---

## 2. Features

- **Dimensional Products:** Adds a boolean flag `Allow Variable Dimensions` on the product template.
- **Price per Square Meter:** Adds a `Price per Sq/m` field on the product template to define the base price for dimensional calculations.
- **Dynamic Price Calculation:** Automatically calculates the `Unit Price` on the sale order line and invoice line using the formula: `Unit Price = Length × Width × Price per Sq/m`.
- **Editable Price per Sq/m:** The `Price per Sq/m` can be overridden on each individual line for pricing flexibility.
- **Sales to Invoice Flow:** When creating an invoice from a sales order, the dimensional data (`Length`, `Width`, `Price per Sq/m`) is automatically and correctly transferred to the invoice line.
- **Standalone Invoices:** The dimensional pricing logic also works on invoices created manually (without a sales order).

---

## 3. Setup and Configuration

1.  **Install the Addon:** Install `sale_dimensions` as a standard Odoo addon.
2.  **Configure a Product:**
    *   Navigate to `Sales > Products > Products` and select or create a product.
    *   Go to the **Sales** tab.
    *   Check the box **`Allow Variable Dimensions`**.
    *   A new field, **`Price per Sq/m`**, will appear. Enter the price for one square meter of this product/service.

---

## 4. Usage

### On Sales Orders

1.  Create a new quotation.
2.  Add a dimensional product.
3.  The fields `Length`, `Width`, and `Price per Sq/m` will appear and be editable.
4.  Enter the desired `Length` and `Width`.
5.  The **`Unit Price`** will be automatically updated.
6.  Enter the number of copies in the **`Quantity`** field.

### On Invoices

- **From a Sales Order:** When you create an invoice from a confirmed sales order, the dimensional data and the calculated unit price will be transferred automatically.
- **Manual Invoice:** You can also create a new invoice, add a dimensional product, and the same logic will apply.

---

## 5. Future Development Roadmap

### Phase 1: Inventory Integration (High Priority)
- **Goal:** Automatically deduct the consumed area from raw material (rolls) inventory.
- **Implementation:** Create a Bill of Materials (BoM) for the printing service. On sales order confirmation, a custom process will create a manufacturing order or stock move that consumes the exact area (`Length x Width x Quantity`) from a specific roll (Lot).

### Phase 2: Wastage Calculation
- **Goal:** Automatically calculate and track material waste.
- **Implementation:** Extend the inventory integration to compare the print width with the roll width and account for the wasted surface area.

### Phase 3: Advanced Pricelist Integration
- **Goal:** Create dynamic pricing rules based on the total area.
- **Implementation:** Develop a deeper integration with Odoo's pricelist engine to allow rules like "5% discount if total area is > 20 m²".

---

---

# إضافة الأبعاد للمبيعات والفواتير (بالعربية)

## 1. الغرض

تقوم هذه الإضافة بتوسيع وظائف تطبيقي المبيعات والفواتير في Odoo للسماح ببيع المنتجات بناءً على الأبعاد (الطول والعرض)، مع حساب السعر بناءً على المساحة. وهي مصممة خصيصًا للشركات التي تبيع خدمات مثل الطباعة، حيث يعتمد السعر على مساحة العمل، وحيث يمكن طلب نسخ متعددة من نفس العنصر.

المنطق الأساسي يغير **سعر الوحدة** في سطر أمر البيع/الفاتورة بناءً على الأبعاد، بينما يظل حقل **الكمية** متاحًا للمستخدم لتحديد عدد النسخ.

---

## 2. الميزات

- **المنتجات ذات الأبعاد:** إضافة علامة `السماح بالأبعاد المتغيرة` في نموذج المنتج.
- **سعر المتر المربع:** إضافة حقل `سعر المتر المربع` في نموذج المنتج لتحديد السعر الأساسي للحسابات.
- **حساب السعر الديناميكي:** حساب `سعر الوحدة` تلقائيًا في سطر أمر البيع والفاتورة باستخدام المعادلة: `سعر الوحدة = الطول × العرض × سعر المتر المربع`.
- **سعر متر مربع قابل للتعديل:** يمكن تعديل `سعر المتر المربع` في كل سطر على حدة لمزيد من المرونة.
- **نقل البيانات من البيع إلى الفاتورة:** عند إنشاء فاتورة من أمر بيع، يتم نقل بيانات الأبعاد والسعر المحسوب تلقائيًا إلى سطر الفاتورة.
- **الفواتير المستقلة:** يعمل منطق تسعير الأبعاد أيضًا على الفواتير التي يتم إنشاؤها يدويًا.

---

## 3. الإعداد والتهيئة

1.  **تثبيت الإضافة:** قم بتثبيت `sale_dimensions` كإضافة قياسية في Odoo.
2.  **تهيئة المنتج:**
    *   اذهب إلى `المبيعات > المنتجات > المنتجات` واختر أو أنشئ منتجًا.
    *   اذهب إلى تبويب **المبيعات**.
    *   قم بتفعيل خيار **`السماح بالأبعاد المتغيرة`**.
    *   سيظهر حقل جديد **`سعر المتر المربع`**. أدخل السعر للمتر المربع الواحد لهذا المنتج/الخدمة.

---

## 4. طريقة الاستخدام

### في أوامر البيع

1.  أنشئ عرض سعر جديد.
2.  أضف منتجًا ذا أبعاد.
3.  ستظهر حقول `الطول` و`العرض` و`سعر المتر المربع` وستكون قابلة للتعديل.
4.  أدخل `الطول` و`العرض` المطلوبين.
5.  سيتم تحديث **`سعر الوحدة`** تلقائيًا.
6.  أدخل عدد النسخ في حقل **`الكمية`**.

### في الفواتير

- **من أمر بيع:** عند إنشاء فاتورة من أمر بيع مؤكد، سيتم نقل بيانات الأبعاد وسعر الوحدة المحسوب تلقائيًا.
- **فاتورة يدوية:** يمكنك أيضًا إنشاء فاتورة جديدة وإضافة منتج ذي أبعاد، وسيتم تطبيق نفس المنطق.

---

## 5. خارطة الطريق المستقبلية

### المرحلة الأولى: التكامل مع المخزون (أولوية عالية)
- **الهدف:** خصم المساحة المستخدمة تلقائيًا من مخزون المواد الخام (الرولات).
- **التنفيذ:** إنشاء قائمة مواد (BoM) لخدمة الطباعة. عند تأكيد أمر البيع، ستقوم عملية مخصصة بإنشاء أمر تصنيع أو حركة مخزون تستهلك المساحة الدقيقة (`الطول × العرض × الكمية`) من رولة معينة (Lot).

### المرحلة الثانية: حساب الهدر
- **الهدف:** حساب وتتبع هدر المواد تلقائيًا.
- **التنفيذ:** توسيع التكامل مع المخزون لمقارنة عرض الطباعة بعرض الرولة وحساب مساحة السطح المهدرة.

### المرحلة الثالثة: تكامل متقدم مع قوائم الأسعار
- **الهدف:** إنشاء قواعد تسعير ديناميكية بناءً على المساحة الإجمالية.
- **التنفيذ:** تطوير تكامل أعمق مع محرك قوائم الأسعار في Odoo للسماح بقواعد مثل "خصم 5% إذا كانت المساحة الإجمالية أكبر من 20 م²".
