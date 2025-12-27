# AI Agent Instructions - Printing Products

## Context
- **Business:** Printing company (banners, flex, stickers)
- **Backend:** Odoo 18 via REST API
- **Language:** Arabic for products, English for technical terms

---

## Golden Rules for Rolls

1. **Unit = Meter (m)** — Never use "Roll" or "Unit"
2. **Attributes = Weight + Width only** — Never add "Length"
3. **Tracking = Lot** — Each roll gets unique barcode

---

## Product Structure

```
Template → Attributes → Variants
رولة بنر → (440g, 3.20m) → MAT-BNR-440-320
```

---

## Attributes

| Name | Values |
|------|--------|
| الوزن | 140g, 240g, 280g, 300g, 340g, 440g |
| عرض الرولة | 1.05m, 1.30m, 1.60m, 2.20m, 3.20m |
| نوع الخامة | ارت فلكس, تورجيت, روكو, سترو |

---

## SKU Format

`[CAT]-[TYPE]-[ATTR1]-[ATTR2]`

- `MAT-BNR-440-320` = Banner 440g 3.20m
- `MAT-FLX-ART-160` = Flex Art 1.60m

---

## API Order

```
1. Attributes → 2. Values → 3. Template → 4. Attribute Lines → 5. Update Variants
```

---

## Validation

✅ **Must:**
- UoM = Meter
- 2 attributes per roll
- tracking = "lot"

❌ **Never:**
- Add "length" as attribute
- Use "Roll" as unit
