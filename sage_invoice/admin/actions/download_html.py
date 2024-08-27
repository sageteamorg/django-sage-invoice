import os
import zipfile
from io import BytesIO

from django.conf import settings
from django.contrib import admin
from django.core.files.storage import default_storage
from django.http import HttpResponse

from sage_invoice.service.invoice_create import QuotationService


@admin.action(description="Download selected report as ZIP file")
def export_as_html(modeladmin, request, queryset):
    service = QuotationService()

    rendered_html = service.render_quotation(queryset)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Write the rendered HTML to the ZIP file
        html_filename = f"invoice_report_{queryset.first().id}.html"
        zip_file.writestr(html_filename, rendered_html)

        # Static files that should be included in the ZIP
        static_files = {
            "assets/css/style.css": "assets/css/style.css",
            "assets/css/style2.css": "assets/css/style2.css",
            "assets/js/jquery.min.js": "assets/js/jquery.min.js",
            "assets/js/jspdf.min.js": "assets/js/jspdf.min.js",
            "assets/js/html2canvas.min.js": "assets/js/html2canvas.min.js",
            "assets/js/main.js": "assets/js/main.js",
        }

        for static_path, archive_path in static_files.items():
            absolute_static_path = os.path.join(
                settings.BASE_DIR, "media", "static", static_path
            )
            if os.path.exists(absolute_static_path):
                with open(absolute_static_path, "rb") as static_file:
                    zip_file.writestr(archive_path, static_file.read())
            else:
                print(f"Static file not found: {absolute_static_path}")

        invoice = queryset.first()

        def add_image_to_zip(image_field, name):
            if image_field:
                with default_storage.open(image_field.name, "rb") as image_file:
                    zip_file.writestr(name, image_file.read())

        add_image_to_zip(invoice.logo, "logo.png")
        add_image_to_zip(invoice.signature, "signature.png")
        add_image_to_zip(invoice.stamp, "stamp.png")

    # Prepare the ZIP file for download
    zip_filename = f"invoice_report_{queryset.first().id}.zip"
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={zip_filename}"

    return response
