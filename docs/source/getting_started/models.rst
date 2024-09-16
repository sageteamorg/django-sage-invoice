Models Layer
============

The models layer defines the database models for various aspects of the invoice management system. These models can be easily integrated into Django's admin interface.

Invoice
-------

The `Invoice` model represents an invoice in the system, capturing essential details like customer information, status, and design elements.

Fields
^^^^^^

- **invoice_date**: The date when the invoice was created.
- **customer_name**: The name of the customer.
- **customer_email**: The email of the customer.
- **status**: The current status of the invoice (e.g., Paid, Unpaid).
- **notes**: Additional notes regarding the invoice.
- **category**: JSONField that allows storing various categories in a dynamic format, such as Terms & Conditions or additional notes.
- **due_date**: The date by which the invoice should be paid.
- **logo**: An image field representing the company logo on the invoice.
- **signature**: The signature image for the invoice.
- **stamp**: The stamp image for the invoice.
- **tracking_code**: Enter the first 3-4 characters of the tracking code. The full code will be auto-generated as <prefix> + <date> + <random number>.
- **template_choice**: Specifies the template used for rendering the invoice.
- **contacts**: JSONField that stores the contact details (e.g., email, phone number) of the customer in a flexible format.

Item
-----------

The `Item` model represents individual items within an invoice, detailing the products or services provided.

Fields
^^^^^^

- **description**: Description of the item.
- **quantity**: The quantity of the item.
- **unit_price**: The price per unit of the item.
- **total_price**: The total price for this item (calculated as quantity * unit price).
- **invoice**: A ForeignKey linking the item to its associated invoice.

Column
-------------

The `Column` model represents custom columns that can be added to individual items in an invoice.

Fields
^^^^^^

- **priority**: The display priority for this column.
- **column_name**: The name of the custom column (e.g., 'Delivery Date', 'Warranty Period').
- **value**: The value for the custom column in the specific invoice.
- **invoice**: The invoice associated with this custom column.
- **item**: The item associated with this custom column.

Expense
-------

The `Expense` model represents calculations for subtotals, taxes, discounts, and totals for an invoice.

Fields
^^^^^^

- **subtotal**: The sum of all item totals.
- **tax_percentage**: The tax percentage applied to the invoice.
- **tax_amount**: The calculated tax amount.
- **discount_percentage**: The discount percentage applied to the invoice.
- **discount_amount**: The calculated discount amount.
- **total_amount**: The final total after applying tax and discount.
- **invoice**: A ForeignKey linking the expense to its associated invoice.

Admin Integration
-----------------

To integrate these models into the Django admin interface, register them in the `admin.py` file of your app.

.. code-block:: python

    from django.contrib import admin
    from sage_invoice.models import Invoice, Item, Column, Expense


    @admin.register(Invoice)
    class InvoiceAdmin(admin.ModelAdmin):
        list_display = ["title", "invoice_date", "customer_name", "status"]


    @admin.register(Item)
    class ItemAdmin(admin.ModelAdmin):
        list_display = ["description", "quantity", "unit_price", "total_price"]


    @admin.register(Column)
    class ColumnAdmin(admin.ModelAdmin):
        list_display = ["column_name", "priority", "value"]


    @admin.register(Expense)
    class ExpenseAdmin(admin.ModelAdmin):
        list_display = ["subtotal", "tax_percentage", "discount_percentage", "total_amount"]

This will allow you to manage the different invoice models directly from the Django admin interface.
