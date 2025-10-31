# Sale & Invoice Dimensions Addon

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
- **Robust Logic:** Uses explicit `@api.onchange` methods to enforce business rules.
- **Dynamic UI:** The dimension-related fields are set to `readonly` for non-dimensional products.

---

## 3. Setup and Configuration

1.  **Install the Addon:** Install `sale_dimensions` as a standard Odoo addon. This will also install the `account` module if it isn't already.
2.  **Configure a Product:**
    *   Navigate to `Sales > Products > Products` and select or create a product.
    *   Go to the **Sales** tab.
    *   Check the box **`Allow Variable Dimensions`**.
    *   A new field, **`Price per Sq/m`**, will appear. Enter the price for one square meter of this product/service.
    *   Save the product.

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

- **From a Sales Order:** When you create an invoice from a confirmed sales order, the dimensional data and the calculated unit price will be transferred automatically to the invoice lines.
- **Manual Invoice:** You can also create a new invoice, add a dimensional product, and the same logic of entering dimensions to calculate the price will apply.

---

## 5. For Future Developers

### Technical Implementation

- **`product.template`:**
    - `allow_variable_dimensions` (Boolean)
    - `price_per_sqm` (Float)

- **`sale.order.line`:**
    - `x_length`, `x_width`, `price_per_sqm` (Float)
    - `allow_variable_dimensions` (Boolean, UI helper)
    - `_onchange_...` methods for price calculation.
    - `_prepare_invoice_line()`: This method is overridden to pass the dimensional data to the `account.move.line` upon invoice creation.

- **`account.move.line`:**
    - Contains the same dimensional fields and `onchange` logic as the `sale.order.line` to allow for standalone invoice creation.

### Important Note on UI Behavior

During development for Odoo 18, it was discovered that dynamic view attributes (`readonly`, `invisible`) are not always reliable inside complex list widgets (`one2many`). The addon relies on a combination of modern view syntax (`readonly="..."`) and robust backend `@api.onchange` logic that forcibly resets values to ensure data integrity, even if the UI doesn't update visually as expected in all cases.