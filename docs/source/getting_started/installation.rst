Installation
============

Installing `django-sage-invoice` is straightforward:

Using `pip` with `virtualenv`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Create a Virtual Environment**:

   .. code-block:: bash

      python -m venv .venv

2. **Activate the Virtual Environment**:

   - On Windows:

     .. code-block:: bash

        .venv\Scripts\activate

   - On macOS/Linux:

     .. code-block:: bash

        source .venv/bin/activate

3. **Install `django-sage-invoice`**:

   .. code-block:: bash

      pip install django-sage-invoice

Using `poetry`
~~~~~~~~~~~~~~

1. **Initialize Poetry** (if not already initialized):

   .. code-block:: bash

      poetry init

2. **Install `django-sage-invoice`**:

   .. code-block:: bash

      poetry add django-sage-invoice

3. **Apply Migrations**:

   After installation, make sure to run the following commands to create the necessary database tables:

   .. code-block:: bash

      python manage.py makemigrations
      python manage.py migrate

Django Settings Configuration
-----------------------------

Installed Apps
~~~~~~~~~~~~~~

To use `django-sage-invoice`, add it to your `INSTALLED_APPS` in the Django settings and configure the `SAGE_MODEL_PREFIX` and `SAGE_MODEL_TEMPLATE`:

.. code-block:: python

   INSTALLED_APPS = [
       # other packages
       "sage_invoice",
   ]
   SAGE_MODEL_PREFIX = "invoice"
   SAGE_MODEL_TEMPLATE = "sage_invoice"

Explanation of `SAGE_MODEL_PREFIX` and `SAGE_MODEL_TEMPLATE`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **SAGE_MODEL_PREFIX**: This setting defines the prefix used to identify your models when searching for Jinja2 templates. By setting `SAGE_MODEL_PREFIX = "invoice"`, the application will look for template files that start with "invoice" in the specified directory.




- **SAGE_MODEL_TEMPLATE**: This setting defines the directory where your model templates are stored. By setting `SAGE_MODEL_TEMPLATE = "sage_invoice"`, the application will search for templates in the `sage_invoice` directory under the specified base directory.

.. warning::

   The `django-sage-invoice` package will not function correctly without configuring both `SAGE_MODEL_PREFIX` and `SAGE_MODEL_TEMPLATE` in your Django settings. Make sure these settings are properly configured to avoid any issues.
