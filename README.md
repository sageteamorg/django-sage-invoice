# Django Sage Invoice

Django Sage Invoice is a Django application for managing invoices, designed to provide essential features required for small businesses to issue invoices, track payments, and manage customer information. The focus of this initial phase is on simplicity and functionality, ensuring that businesses can use the system without being overwhelmed by advanced or complex features.

The system offers a robust admin interface to create, view, and manage invoices along with their related components, such as categories, items, and totals. The primary objectives are to ensure that businesses can efficiently issue invoices, monitor payment status, and handle basic customer management tasks, making it an accessible solution for small-scale operations.

#### **Key Features:**

1. **Basic Invoicing**
   - Create and send professional invoices manually.
   - Customizable invoice templates with basic branding (logo, company info).
   - Invoice status tracking (draft, sent, paid).
2. **Customer Management**
   - Add and manage customer profiles.
   - Support for basic customer contact and billing information.
3. **Basic Payments Tracking**
   - Manual recording of payments (bank transfer, cash).
   - Partial payments support.
4. **Basic Tax Support**
   - Add tax rates manually (VAT, GST, etc.).
   - Apply taxes to invoices and show breakdown.
5. **Basic Reports**
   - Export invoices in PDF format.
   - Basic reporting on unpaid/paid invoices.


## Installation

### Using `pip` with `virtualenv`

1. **Create a Virtual Environment**:

    ```bash
    python -m venv .venv
    ```

2. **Activate the Virtual Environment**:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

3. **Install `django-sage-invoice`**:

    ```bash
    pip install django-sage-invoice
    ```

### Using `poetry`

1. **Initialize Poetry** (if not already initialized):

    ```bash
    poetry init
    ```

2. **Install `django-sage-invoice`**:

    ```bash
    poetry add django-sage-invoice
    ```

3. **Apply Migrations**:

    After installation, make sure to run the following commands to create the necessary database tables:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Configuration

### Django Settings

Add `django-sage-invoice` to your `INSTALLED_APPS` in the Django settings and configure the `SAGE_MODEL_PREFIX` and `SAGE_MODEL_TEMPLATE`:

```python
INSTALLED_APPS = [
    # other packages
    "sage_tools",
    "sage_invoice",
]
SAGE_MODEL_PREFIX = "invoice"
SAGE_MODEL_TEMPLATE = "sage_invoice"
```
