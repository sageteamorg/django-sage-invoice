# Django Sage Invoice

Django Sage Invoice is a Django application for managing invoices. It provides a robust admin interface to create, view, and manage invoices and their related components like categories, items, and totals.

## Features

- Create and manage invoices with detailed customer information.
- Customize invoices with logos, backgrounds, signatures, and stamps.
- Add custom columns to each invoice for additional information.
- Generate invoice totals automatically, including tax and discount calculations.
- Export invoices as HTML files bundled in a ZIP archive.
- Choose from predefined templates or define your own.

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

Add `django-sage-invoice` to your `INSTALLED_APPS` in the Django settings and configure the `MODEL_PREFIX` and `MODEL_TEMPLATE`:

```python
INSTALLED_APPS = [
    ...
    "sage_invoice",
    ...
]
MODEL_PREFIX = "invoice"
MODEL_TEMPLATE = "sage_invoice"
```