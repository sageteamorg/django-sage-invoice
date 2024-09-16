import pytest
import secrets
from datetime import datetime
from unittest import mock
from sage_invoice.helpers.funcs import get_template_choices, generate_tracking_code
from sage_invoice.service.discovery import JinjaTemplateDiscovery


@pytest.mark.django_db
class TestHelperFunctions:

    @mock.patch("sage_invoice.helpers.funcs.JinjaTemplateDiscovery")
    @mock.patch("sage_invoice.helpers.funcs.settings")
    def test_get_template_choices_for_invoice(self, mock_settings, mock_discovery):
        """Test template choices for an invoice (non-receipt)."""
        mock_settings.SAGE_MODEL_TEMPLATE = "sage_invoice"
        mock_discovery_instance = mock_discovery.return_value
        mock_discovery_instance.SAGE_MODEL_TEMPLATEs = {
            "template1": "/path/to/template1.jinja2",
            "template2": "/path/to/template2.jinja2"
        }

        choices = get_template_choices(is_receipt=False)

        assert len(choices) == 2
        assert choices[0][0] == "template1"
        assert choices[0][1] == "Template1 Template"
        assert choices[1][0] == "template2"
        assert choices[1][1] == "Template2 Template"

    @mock.patch("sage_invoice.helpers.funcs.JinjaTemplateDiscovery")
    @mock.patch("sage_invoice.helpers.funcs.settings")
    def test_get_template_choices_for_receipt(self, mock_settings, mock_discovery):
        """Test template choices for a receipt."""
        mock_settings.SAGE_MODEL_TEMPLATE = "sage_invoice"
        mock_discovery_instance = mock_discovery.return_value
        mock_discovery_instance.receipt_templates = {
            "receipt1": "/path/to/receipt1.jinja2",
            "receipt2": "/path/to/receipt2.jinja2"
        }

        choices = get_template_choices(is_receipt=True)

        assert len(choices) == 2
        assert choices[0][0] == "receipt1"
        assert choices[0][1] == "Receipt1 Template"
        assert choices[1][0] == "receipt2"
        assert choices[1][1] == "Receipt2 Template"

    def test_get_template_choices_no_templates(self):
        """Test when no templates are available."""
        with mock.patch("sage_invoice.helpers.funcs.JinjaTemplateDiscovery") as mock_discovery:
            mock_discovery_instance = mock_discovery.return_value
            mock_discovery_instance.SAGE_MODEL_TEMPLATEs = {}
            mock_discovery_instance.receipt_templates = {}

            choices = get_template_choices(is_receipt=False)
            assert choices == [("", "No Templates Available")]

    @mock.patch("secrets.randbelow", return_value=1234)
    def test_generate_tracking_code(self, mock_randbelow):
        """Test the tracking code generation."""
        user_input = "INV"
        creation_date = datetime(2024, 9, 1)

        tracking_code = generate_tracking_code(user_input, creation_date)

        assert tracking_code is not None
        mock_randbelow.assert_called_once_with(8000)
