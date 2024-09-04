Models Layer
============

The models layer defines the database models for various aspects of the invoice management system. These models can be easily integrated into Django's admin interface.

Invoice
-------

The `Invoice` model represents an invoice in the system, capturing essential details like customer information, status, and design elements.

Fields
^^^^^^

- `invoice_date`: The date when the invoice was created.
- `customer_name`: The name of the customer.
- `customer_email`: The email of the customer.
- `status`: The current status of the invoice (e.g., Paid, Unpaid).
- `notes`: Additional notes regarding the invoice.
- `category`: The category associated with this invoice.
- `due_date`: The date by which the invoice should be paid.
- `logo`: The logo displayed on the invoice.
- `signature`: The signature image for the invoice.
- `stamp`: The stamp image for the invoice.
- `template_choice`: The template used for rendering the invoice.

InvoiceCategory
---------------

The `InvoiceCategory` model represents categories that can be associated with invoices, helping to organize and classify them.

Fields
^^^^^^

- `title`: The title of the category.
- `description`: A description of the category.

InvoiceItem
-----------

The `InvoiceItem` model represents individual items within an invoice, detailing the products or services provided.

Fields
^^^^^^

- `description`: Description of the item.
- `quantity`: The quantity of the item.
- `unit_price`: The price per unit of the item.
- `total_price`: The total price for this item (calculated as quantity * unit price).
- `invoice`: The invoice associated with this item.

InvoiceColumn
-------------

The `InvoiceColumn` model represents custom columns that can be added to individual items in an invoice.

Fields
^^^^^^

- `priority`: The priority associated with each custom column.
- `column_name`: The name of the custom column (e.g., 'Delivery Date', 'Warranty Period').
- `value`: The value for the custom column in the specific invoice.
- `invoice`: The invoice associated with this custom column.
- `item`: The item associated with this custom column.

InvoiceTotal
------------

The `InvoiceTotal` model represents the total amount for an invoice, including calculations for tax, discounts, and the final total.

Fields
^^^^^^

- `subtotal`: The sum of all item totals.
- `tax_percentage`: The tax percentage applied to the invoice.
- `discount_percentage`: The discount percentage applied to the invoice.
- `tax_amount`: The calculated tax amount.
- `discount_amount`: The calculated discount amount.
- `total_amount`: The final total after applying tax and discount.
- `invoice`: The invoice associated with this total.

Admin Integration
-----------------

To integrate these models into the Django admin interface, register them in the `admin.py` file of your app.

.. code-block:: python

    from django.contrib import admin
    from sage_invoice.models import (
        Invoice,
        InvoiceCategory,
        InvoiceItem,
        InvoiceColumn,
        InvoiceTotal,
    )


    @admin.register(Invoice)
    class InvoiceAdmin(admin.ModelAdmin):
        list_display = ["title", "invoice_date", "customer_name", "status"]


    @admin.register(InvoiceCategory)
    class InvoiceCategoryAdmin(admin.ModelAdmin):
        list_display = ["title", "description"]


    @admin.register(InvoiceItem)
    class InvoiceItemAdmin(admin.ModelAdmin):
        list_display = ["description", "quantity", "unit_price", "total_price"]


    @admin.register(InvoiceColumn)
    class InvoiceColumnAdmin(admin.ModelAdmin):
        list_display = ["column_name", "priority", "value"]


    @admin.register(InvoiceTotal)
    class InvoiceTotalAdmin(admin.ModelAdmin):
        list_display = ["subtotal", "tax_percentage", "discount_percentage", "total_amount"]

This will allow you to manage the different invoice models directly from the Django admin interface.
