# Sale Dimensions Addon

## 1. Purpose

This addon extends the functionality of the Odoo Sales application to allow selling products based on dimensions (length and width), with the price calculated based on the area. It is specifically designed for businesses that sell services like printing, where the price depends on the surface area of the job, and where multiple copies of the same dimensional item might be ordered.

The core logic changes the **Unit Price** of the sale order line based on the dimensions, while the **Quantity** field remains available for the user to specify the number of copies.

---

## 2. Features

- **Dimensional Products:** Adds a boolean flag `Allow Variable Dimensions` on the product template.
- **Price per Square Meter:** Adds a `Price per Sq/m` field on the product template to define the base price for dimensional calculations.
- **Dynamic Price Calculation:** Automatically calculates the `Unit Price` on the sale order line using the formula: `Unit Price = Length × Width × Price per Sq/m`.
- **Editable Price per Sq/m:** The `Price per Sq/m` can be overridden on each individual sale order line for pricing flexibility.
- **Robust Logic:** Uses explicit `@api.onchange` methods to enforce business rules, ensuring that dimensions and prices for non-dimensional products are reset to zero.
- **Dynamic UI:** The dimension-related fields on the sale order line (`Length`, `Width`, `Price per Sq/m`) are set to `readonly` for non-dimensional products.

---

## 3. Setup and Configuration

1.  **Install the Addon:** Install `sale_dimensions` as a standard Odoo addon.
2.  **Configure a Product:**
    *   Navigate to `Sales > Products > Products` and select or create a product you want to sell by dimension.
    *   Go to the **Sales** tab.
    *   Check the box **`Allow Variable Dimensions`**.
    *   A new field, **`Price per Sq/m`**, will appear. Enter the price for one square meter of this product/service.
    *   Save the product.

---

## 4. Usage

1.  **Create a Sales Order:** Navigate to the Sales application and create a new quotation.
2.  **Add a Dimensional Product:**
    *   Add the product you configured above.
    *   The fields `Length`, `Width`, and `Price per Sq/m` will appear on the line and be editable.
    *   The `Price per Sq/m` will be pre-filled with the value from the product form.
    *   Enter the desired `Length` and `Width`.
    *   The **`Unit Price`** will be automatically and instantly updated based on the formula.
    *   Enter the number of copies in the **`Quantity`** field.
    *   The `Subtotal` will be calculated correctly by Odoo (`Unit Price` × `Quantity`).
3.  **Add a Normal Product:**
    *   Add any standard product that does not have `Allow Variable Dimensions` checked.
    *   The `Length`, `Width`, and `Price per Sq/m` fields will be visible but **read-only** and set to `0.0`. The standard pricing mechanism will apply.

---

## 5. For Future Developers

### Technical Implementation

- **`product.template`:**
    - `allow_variable_dimensions` (Boolean): Controls the feature.
    - `price_per_sqm` (Float): Stores the default price per area.

- **`sale.order.line`:**
    - `allow_variable_dimensions` (Boolean): A non-stored field whose value is set via onchange for UI control.
    - `x_length`, `x_width` (Float): The dimensional inputs.
    - `price_per_sqm` (Float): The editable price per area for the line, defaults to the product's value.

- **Key Methods (`models/sale_order.py`):**
    - `@api.onchange('product_id') _onchange_product_id_dimensions()`: This is the main trigger. It checks the selected product and sets the `allow_variable_dimensions` flag on the line, preparing it for dimensional input. It also resets values for non-dimensional products.
    - `@api.onchange('x_length', 'x_width', 'price_per_sqm') _onchange_dimensions_price()`: This method calculates the `price_unit`. It also contains a **robustness check** to forcibly reset dimension values if a user attempts to change them for a non-dimensional product. This was implemented as a workaround for UI limitations.

### Important Note on UI Behavior (`attrs` vs. direct attributes)

During the development of this module for Odoo 18, it was discovered that the traditional `attrs` attribute on fields does not reliably work for dynamic UI changes within the new `sol_o2m` (list) widget. The final implementation uses the modern direct attribute syntax (e.g., `readonly="not allow_variable_dimensions"`). The responsiveness of this depends on the `allow_variable_dimensions` field being correctly updated on the client side, which is handled by the `_onchange_product_id_dimensions` method. The backend Python logic provides a final guarantee of data integrity in case the UI does not respond as expected.
