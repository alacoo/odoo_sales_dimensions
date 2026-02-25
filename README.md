# Sale & Invoice Dimensions Addon

This document is also available in Arabic below.

---

## 1. Purpose

This addon extends Odoo Sales and Invoicing to enable selling products based on dimensions (Length × Width), with the price calculated per square meter. Designed for printing businesses where pricing depends on the surface area of the print job.

The **Unit Price** is computed from dimensions, while the **Quantity** field is used for number of copies.

---

## 2. Features

- **Dimensional Products:** `Allow Variable Dimensions` flag on product template
- **Price per Square Meter:** `Price per Sq/m` field for base pricing
- **Roll Width:** `Roll Width (m)` field on product template for raw materials
- **Production Margin:** `Production Margin (m)` field for waste/margin calculation
- **Roll Length:** `Roll Length (m)` field for inventory calculations
- **Dynamic Price Calculation:** `Unit Price = Length × Width × Price per Sq/m`
- **Editable Price per Sq/m:** Override on each individual line
- **SO to Invoice Flow:** Dimensional data transfers correctly to invoice lines
- **Standalone Invoices:** Dimensional pricing works on manual invoices

---

## 3. Fields Reference

### On `product.template`

| Field | Type | Description |
|-------|------|-------------|
| `allow_variable_dimensions` | Boolean | Enable dimensional pricing |
| `price_per_sqm` | Float | Base price per square meter (for sales) |
| `x_width` | Float | Roll width in meters (e.g. 1.60) |
| `production_margin` | Float | Extra margin in meters for waste |
| `roll_length` | Float | Default roll length in meters (default: 50) |

### On `sale.order.line` / `account.move.line`

| Field | Type | Description |
|-------|------|-------------|
| `x_length` | Float | Print length in meters |
| `x_width` | Float | Print width in meters |
| `price_per_sqm` | Float | Price per sq/m (copied from product) |
| `allow_variable_dimensions` | Boolean | Whether line uses dimensional pricing |

---

## 4. Setup and Configuration

1. Install `ala_odoo_dimensions`
2. Navigate to `Sales > Products > Products`
3. Check **`Allow Variable Dimensions`**
4. Enter **`Price per Sq/m`** (sell price)
5. For raw materials (rolls), also fill:
   - **`Roll Width`** — width in meters (e.g. `1.60`)
   - **`Roll Length`** — default length (e.g. `50`)
   - **`Production Margin`** — waste margin (e.g. `0.05`)

---

## 5. Usage

### On Sales Orders

1. Create a new quotation
2. Add a dimensional product
3. `Length`, `Width`, and `Price per Sq/m` fields appear
4. Enter `Length` and `Width`
5. **Unit Price** updates automatically: `L × W × Price/Sqm`
6. Enter number of copies in **Quantity**

### On Invoices

- **From SO:** Dimensional data transfers automatically
- **Manual:** Same dimensional logic applies

---

## 6. Cost Calculation for Materials

For raw material (roll) products, the cost structure is:

```
standard_price = cost per linear meter
cost_per_sqm   = standard_price / x_width
roll_cost      = standard_price × actual_roll_length
```

**Example:** Banner Roll 280g / 1.60m width

```
standard_price = 490 YER/m (linear meter cost)
cost_per_sqm   = 490 / 1.60 = 306.25 YER/m²
Roll of 50m    = 490 × 50 = 24,500 YER
Roll of 30m    = 490 × 30 = 14,700 YER
```

---

## 7. Development Roadmap

### ✅ Phase 1: Foundation (Current)

- [x] Dimensional pricing on Sales & Invoices
- [x] `x_width` field on `product.template` for roll width
- [x] `production_margin` for waste calculation
- [x] `roll_length` for inventory planning

### ⬜ Phase 2: Inventory Integration

- [ ] Auto-deduct consumed length from roll Lots
- [ ] `cost_per_sqm` as computed field: `standard_price / x_width`
- [ ] Bill of Materials linking services to materials + inks

### ⬜ Phase 3: Smart Pricing

- [ ] Pricelist integration with `price_per_sqm`
- [ ] Area-based discount rules (e.g. >20m² = 5% off)
- [ ] Customer-specific pricing per sq/m

### ⬜ Phase 4: Reports & Analytics

- [ ] Material consumption report (per roll, per Lot)
- [ ] Waste/scrap percentage tracking
- [ ] Profit margin analysis (sell price vs material cost per job)
- [ ] Roll inventory forecasting

---

---

# إضافة الأبعاد للمبيعات والفواتير (بالعربية)

## 1. الغرض

تُوسّع هذه الإضافة وظائف المبيعات والفواتير في Odoo للسماح ببيع المنتجات بناءً على الأبعاد (الطول والعرض)، مع حساب السعر بناءً على المساحة (متر مربع).

المنطق الأساسي: **سعر الوحدة = الطول × العرض × سعر المتر المربع**

حقل **الكمية** يبقى متاحاً لعدد النسخ.

---

## 2. الحقول المضافة

### على المنتج (`product.template`)

| الحقل | الوصف | مثال |
|-------|-------|------|
| `allow_variable_dimensions` | تفعيل التسعير بالأبعاد | ✅ |
| `price_per_sqm` | سعر البيع للمتر المربع | 150 ر.ي |
| `x_width` | عرض الرولة بالمتر | 1.60 |
| `production_margin` | هامش الهدر بالمتر | 0.05 |
| `roll_length` | طول الرولة الافتراضي | 50 |

---

## 3. حساب التكاليف للخامات

```
سعر المتر الطولي (standard_price) = تكلفة الشراء / الطول الفعلي
تكلفة المتر المربع = سعر_المتر_الطولي ÷ عرض_الرولة
تكلفة الرولة = سعر_المتر_الطولي × الطول_الفعلي
```

**مثال:** رولة بنر 280g عرض 1.60م

```
سعر المتر الطولي  = 490 ريال
تكلفة المتر المربع = 490 ÷ 1.60 = 306.25 ريال/م²
رولة 50م          = 490 × 50 = 24,500 ريال
رولة 30م          = 490 × 30 = 14,700 ريال
```

---

## 4. خارطة الطريق

### ✅ المرحلة 1: الأساسيات (الحالية)

- [x] التسعير بالأبعاد في المبيعات والفواتير
- [x] حقل `x_width` على المنتج لعرض الرولة
- [x] حقل `production_margin` للهدر
- [x] وحدة القياس = متر طولي (للتتبع الدقيق)

### ⬜ المرحلة 2: ربط المخزون

- [ ] خصم الطول المستخدم تلقائياً من الـ Lot
- [ ] `cost_per_sqm` حقل محسوب تلقائياً
- [ ] قوائم مواد (BoM) تربط الخدمات بالخامات

### ⬜ المرحلة 3: التسعير الذكي

- [ ] تكامل قوائم الأسعار مع `price_per_sqm`
- [ ] خصومات حسب المساحة الإجمالية
- [ ] أسعار خاصة لكل عميل

### ⬜ المرحلة 4: التقارير والتحليلات

- [ ] تقرير استهلاك الخامات (لكل رولة / Lot)
- [ ] تتبع نسبة الهدر
- [ ] تحليل هامش الربح (سعر البيع vs تكلفة الخامة)
- [ ] توقعات مخزون الرولات
