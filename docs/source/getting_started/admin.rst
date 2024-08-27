Admin Layer
===========

The admin layer customizes the Django admin interface to manage invoices efficiently. This section explains how to configure and manage invoices and related categories using the Django admin interface.

Managing Invoices
-----------------

In the Django admin interface, you can manage various aspects of invoices, including creating, editing, and deleting them.

Viewing Invoices
----------------

To view the list of invoices:

1. Navigate to the Django admin interface.

.. image:: ../../_static/1.png
   :alt: Viewing Invoices

This will display a list of all invoices, where you can select and manage them.

Creating a New Invoice
-----------------------

To create a new invoice:

1. Click on the `Add Invoice` button on the top right.
2. Fill in the basic details for the invoice, such as title, date, and customer information.

.. image:: ../../_static/2.png
   :alt: Adding a New Invoice

3. Assign the invoice to a category. If you haven't created a category yet, you need to create one first.

.. image:: ../../_static/3.png
   :alt: Assigning a Category to an Invoice

4. Select design elements like logo, background, signature, and stamp.


5. Choose a template for the invoice. The system comes with three pre-defined templates, but you can create your own custom templates as well.

.. image:: ../../_static/4.png
   :alt: Selecting a Template for the Invoice

6. After saving the invoice, you can add custom columns to include additional details like delivery date or warranty period.

.. image:: ../../_static/5.png
   :alt: Adding a custom columns

.. note::
   Custom columns can only be added after the invoice has been created.

Showing an Invoice
------------------

To show the details of an existing invoice:

1. Select an invoice from the list.

2. Choose the `Show selected invoice` action from the dropdown menu.

.. image:: ../../_static/6.png
   :alt: Selecting an Invoice

3. This will display the invoice details in a printable format.

.. image:: ../../_static/7.png
   :alt: Showing the Selected Invoice
   
.. image:: ../../_static/8.png
   :alt: Print the Selected Invoice

Exporting Invoices
------------------

The Django admin interface also allows you to export invoices as HTML files bundled in a ZIP archive.

1. Select one or more invoices from the list.
2. Choose the `Download selected report as ZIP file` action from the dropdown menu.

.. image:: ../../_static/9.png
   :alt: Exporting Invoices

3. The ZIP file will include the invoice(s) and any associated static files like logos or signatures.

.. image:: ../../_static/10.png
   :alt: Downloaded ZIP File
