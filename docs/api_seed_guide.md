# Odoo Product Seeding Guide for Developers

This guide explains how to seed demo data for printing materials (Rolls, Banners, Stickers, Equipment) via Odoo REST API.

---

## Important: Execution Order

Data must be created in this exact order to avoid dependency errors:

```
1. Product Attributes (الخصائص)
       ↓
2. Attribute Values (قيم الخصائص)
       ↓
3. Product Templates (قوالب المنتجات)
       ↓
4. Attribute Lines (ربط الخصائص بالقوالب)
       ↓
5. Product Variants (المتغيرات) - Auto-generated, then update prices
```

---

## API Endpoints Overview

| Model | Endpoint | Description |
|-------|----------|-------------|
| `product.attribute` | `/api/product.attribute` | Product attributes (Weight, Width, etc.) |
| `product.attribute.value` | `/api/product.attribute.value` | Attribute values (440g, 3.20m, etc.) |
| `product.template` | `/api/product.template` | Product templates (Banner Roll, Flex Roll) |
| `product.template.attribute.line` | `/api/product.template.attribute.line` | Link attributes to templates |
| `product.product` | `/api/product.product` | Product variants (auto-created) |

---

## Step 1: Create Product Attributes

### Attributes to Create:

| name | display_type | create_variant |
|------|--------------|----------------|
| الوزن | pills | always |
| عرض الرولة | pills | always |
| نوع الخامة | pills | always |
| اللون | radio | always |
| السماكة | pills | always |

### API Request:

```http
POST /api/product.attribute
Content-Type: application/json
```

```json
{
  "name": "الوزن",
  "display_type": "pills",
  "create_variant": "always"
}
```

### Response:
```json
{
  "id": 1,
  "name": "الوزن"
}
```

**Save the returned `id` - you'll need it for attribute values.**

---

## Step 2: Create Attribute Values

### Values for "الوزن" (Weight):

| name | attribute_id |
|------|--------------|
| 240g | (weight_attr_id) |
| 280g | (weight_attr_id) |
| 300g | (weight_attr_id) |
| 340g | (weight_attr_id) |
| 440g | (weight_attr_id) |
| 450g | (weight_attr_id) |

### Values for "عرض الرولة" (Roll Width):

| name | attribute_id |
|------|--------------|
| 1.05m | (width_attr_id) |
| 1.10m | (width_attr_id) |
| 1.27m | (width_attr_id) |
| 1.30m | (width_attr_id) |
| 1.52m | (width_attr_id) |
| 1.55m | (width_attr_id) |
| 1.60m | (width_attr_id) |
| 2.02m | (width_attr_id) |
| 2.20m | (width_attr_id) |
| 2.60m | (width_attr_id) |
| 3.20m | (width_attr_id) |

### Values for "نوع الخامة" (Material Type):

| name | attribute_id |
|------|--------------|
| ارت فلكس | (material_attr_id) |
| تورجيت | (material_attr_id) |
| روكو (ROGO) | (material_attr_id) |
| سترو (SETRO) | (material_attr_id) |
| شفاف | (material_attr_id) |

### API Request:

```http
POST /api/product.attribute.value
Content-Type: application/json
```

```json
{
  "name": "440g",
  "attribute_id": 1
}
```

---

## Step 3: Create Product Templates

### Templates to Create:

| name | detailed_type | uom_id | categ_id |
|------|---------------|--------|----------|
| رولة طباعة بنر (Banner Roll) | product | m (meter) | Raw Materials |
| رولة طباعة فلكس (Flex Roll) | product | m (meter) | Raw Materials |
| رولة لاصق ستيكر (Sticker Roll) | product | m (meter) | Raw Materials |

### API Request:

```http
POST /api/product.template
Content-Type: application/json
```

```json
{
  "name": "رولة طباعة بنر (Banner Roll)",
  "detailed_type": "product",
  "uom_id": 3,
  "uom_po_id": 3,
  "allow_variable_dimensions": false,
  "tracking": "lot"
}
```

**Note:** `uom_id: 3` is typically "Meter" in Odoo. Verify with: `GET /api/uom.uom?domain=[('name','ilike','meter')]`

---

## Step 4: Link Attributes to Templates

After creating templates, link them to their attributes.

### For Banner Roll:
- Link to "الوزن" with values: 280g, 300g, 340g, 440g, 450g
- Link to "عرض الرولة" with values: 1.05m, 1.30m, 1.55m, 2.20m, 2.60m, 3.20m

### For Flex Roll:
- Link to "نوع الخامة" with values: ارت فلكس, تورجيت
- Link to "عرض الرولة" with values: 1.10m, 1.30m, 1.60m, 2.20m, 2.60m, 3.20m

### API Request:

```http
POST /api/product.template.attribute.line
Content-Type: application/json
```

```json
{
  "product_tmpl_id": 1,
  "attribute_id": 1,
  "value_ids": [[6, 0, [1, 2, 3, 4, 5]]]
}
```

**Note:** `value_ids` uses Odoo's special command format:
- `[6, 0, [list_of_ids]]` = Replace all with these IDs

---

## Step 5: Update Product Variants

After linking attributes, Odoo automatically creates variants. Now update each variant with:
- `default_code` (Internal Reference/SKU)
- `standard_price` (Cost)
- `variant_price_per_sqm` (Our custom field for selling price per sqm)

### Variant Data - Banner Rolls:

| Variant | default_code | standard_price | variant_price_per_sqm |
|---------|--------------|----------------|----------------------|
| رولة بنر (280g, 1.05m) | MAT-BNR-280-105 | 0.63 | 1.50 |
| رولة بنر (280g, 1.30m) | MAT-BNR-280-130 | 0.78 | 1.50 |
| رولة بنر (280g, 3.20m) | MAT-BNR-280-320 | 1.92 | 1.50 |
| رولة بنر (300g, 1.05m) | MAT-BNR-300-105 | 0.63 | 1.80 |
| رولة بنر (300g, 3.20m) | MAT-BNR-300-320 | 1.92 | 1.80 |
| رولة بنر (440g, 1.60m) | MAT-BNR-440-160 | 1.36 | 2.50 |
| رولة بنر (440g, 2.20m) | MAT-BNR-440-220 | 1.87 | 2.50 |
| رولة بنر (440g, 3.20m) | MAT-BNR-440-320 | 2.72 | 2.50 |

### Variant Data - Flex Rolls:

| Variant | default_code | standard_price | variant_price_per_sqm |
|---------|--------------|----------------|----------------------|
| رولة فلكس (ارت فلكس, 1.10m) | MAT-FLX-ART-110 | 1.98 | 4.00 |
| رولة فلكس (ارت فلكس, 1.60m) | MAT-FLX-ART-160 | 2.88 | 4.00 |
| رولة فلكس (ارت فلكس, 3.20m) | MAT-FLX-ART-320 | 5.76 | 4.00 |
| رولة فلكس (تورجيت, 1.60m) | MAT-FLX-TRG-160 | 3.20 | 5.00 |
| رولة فلكس (تورجيت, 3.20m) | MAT-FLX-TRG-320 | 6.40 | 5.00 |

### API Request (Find and Update Variant):

First, find the variant by template and attribute values:

```http
GET /api/product.product?domain=[('product_tmpl_id','=',1),('product_template_attribute_value_ids.name','in',['440g','3.20m'])]
```

Then update:

```http
PUT /api/product.product/123
Content-Type: application/json
```

```json
{
  "default_code": "MAT-BNR-440-320",
  "standard_price": 2.72,
  "variant_price_per_sqm": 2.50
}
```

---

## Complete Seed Script Example (Pseudo-code)

```javascript
async function seedPrintingProducts() {
  // Step 1: Create Attributes
  const weightAttr = await createAttribute("الوزن", "pills", "always");
  const widthAttr = await createAttribute("عرض الرولة", "pills", "always");
  const materialAttr = await createAttribute("نوع الخامة", "pills", "always");

  // Step 2: Create Attribute Values
  const weights = ["240g", "280g", "300g", "340g", "440g", "450g"];
  const weightValues = await Promise.all(
    weights.map(w => createAttributeValue(w, weightAttr.id))
  );

  const widths = ["1.05m", "1.30m", "1.60m", "2.20m", "3.20m"];
  const widthValues = await Promise.all(
    widths.map(w => createAttributeValue(w, widthAttr.id))
  );

  // Step 3: Create Product Template
  const bannerRoll = await createProductTemplate({
    name: "رولة طباعة بنر (Banner Roll)",
    detailed_type: "product",
    uom_id: METER_UOM_ID,
    tracking: "lot"
  });

  // Step 4: Link Attributes to Template
  await createAttributeLine(bannerRoll.id, weightAttr.id, weightValues.map(v => v.id));
  await createAttributeLine(bannerRoll.id, widthAttr.id, widthValues.map(v => v.id));

  // Step 5: Wait for variants to be created, then update
  await sleep(2000); // Give Odoo time to create variants
  
  const variants = await getVariants(bannerRoll.id);
  for (const variant of variants) {
    const code = generateCode(variant);
    const cost = calculateCost(variant);
    await updateVariant(variant.id, { default_code: code, standard_price: cost });
  }
}
```

---

## Custom Fields Reference

Our `odoo_sales_dimensions` module adds these custom fields:

### On `product.template`:
| Field | Type | Description |
|-------|------|-------------|
| `allow_variable_dimensions` | Boolean | Enable dimensional pricing |
| `price_per_sqm` | Float | Base price per square meter |
| `production_margin` | Float | Extra length for production waste |

### On `product.product`:
| Field | Type | Description |
|-------|------|-------------|
| `variant_price_per_sqm` | Float | Variant-specific price per sqm (overrides template) |

---

## Sample JSON: Complete Banner Roll Creation

```json
{
  "attributes": [
    {
      "name": "الوزن",
      "display_type": "pills",
      "create_variant": "always",
      "values": ["280g", "300g", "440g"]
    },
    {
      "name": "عرض الرولة",
      "display_type": "pills", 
      "create_variant": "always",
      "values": ["1.60m", "2.20m", "3.20m"]
    }
  ],
  "template": {
    "name": "رولة طباعة بنر (Banner Roll)",
    "detailed_type": "product",
    "uom_name": "m",
    "category": "Raw Materials",
    "tracking": "lot",
    "allow_variable_dimensions": false
  },
  "variants": [
    { "attrs": ["280g", "1.60m"], "code": "MAT-BNR-280-160", "cost": 0.96 },
    { "attrs": ["280g", "2.20m"], "code": "MAT-BNR-280-220", "cost": 1.32 },
    { "attrs": ["280g", "3.20m"], "code": "MAT-BNR-280-320", "cost": 1.92 },
    { "attrs": ["300g", "1.60m"], "code": "MAT-BNR-300-160", "cost": 0.96 },
    { "attrs": ["300g", "2.20m"], "code": "MAT-BNR-300-220", "cost": 1.32 },
    { "attrs": ["300g", "3.20m"], "code": "MAT-BNR-300-320", "cost": 1.92 },
    { "attrs": ["440g", "1.60m"], "code": "MAT-BNR-440-160", "cost": 1.36 },
    { "attrs": ["440g", "2.20m"], "code": "MAT-BNR-440-220", "cost": 1.87 },
    { "attrs": ["440g", "3.20m"], "code": "MAT-BNR-440-320", "cost": 2.72 }
  ]
}
```

---

## Notes for Developers

1. **UoM IDs**: Always verify unit of measure IDs in target system. "Meter" is typically ID 3, but may vary.

2. **Attribute Value Commands**: Odoo uses special tuple commands for Many2many fields:
   - `[6, 0, [ids]]` = Replace all
   - `[4, id]` = Add one
   - `[3, id]` = Remove one

3. **Variant Creation**: Variants are auto-created when attribute lines are added. Wait ~2 seconds before querying.

4. **Tracking**: Set `tracking: "lot"` for rolls to enable QR/Barcode tracking per roll.

5. **Custom Fields**: The `variant_price_per_sqm` field is from our custom module. Ensure `odoo_sales_dimensions` is installed.
