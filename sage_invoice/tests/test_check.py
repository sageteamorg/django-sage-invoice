import pytest
from django.conf import settings

from sage_invoice.check import (
    check_installed_apps,
    check_required_libraries,
    check_required_settings,
)


@pytest.mark.django_db
class TestSystemChecks:

    @pytest.fixture
    def reset_settings(self):
        """Fixture to reset settings after each test."""
        original_settings = settings.INSTALLED_APPS[:]
        yield
        settings.INSTALLED_APPS = original_settings

    def test_check_installed_apps_success(self, reset_settings):
        settings.INSTALLED_APPS = list(settings.INSTALLED_APPS) + ["sage_invoice"]
        errors = check_installed_apps(None)
        assert errors == []

    def test_check_installed_apps_failure(self, reset_settings):
        settings.INSTALLED_APPS = []
        errors = check_installed_apps(None)
        assert len(errors) == 1
        assert errors[0].id == "sage_invoice.E001"
        assert errors[0].msg == "'sage_invoice' is missing in INSTALLED_APPS."

    @pytest.fixture
    def mock_find_spec(self, monkeypatch):
        """Fixture to mock find_spec."""

        def mock_spec(name):
            if name == "sage_invoice":
                return True
            return None

        monkeypatch.setattr("importlib.util.find_spec", mock_spec)

    def test_check_required_libraries_success(self, mock_find_spec):
        errors = check_required_libraries(None)
        assert errors == []

    def test_check_required_libraries_failure(self, monkeypatch):

        def mock_spec(name):
            return None  # Simulate library not being installed

        monkeypatch.setattr("importlib.util.find_spec", mock_spec)
        errors = check_required_libraries(None)
        assert len(errors) == 0

    def test_check_required_settings_success(self):
        settings.SAGE_MODEL_PREFIX = "invoice"
        settings.SAGE_MODEL_TEMPLATE = "sage_invoice"
        errors = check_required_settings(None)
        assert errors == []

    def test_check_required_settings_failure(self):
        if hasattr(settings, "SAGE_MODEL_PREFIX"):
            del settings.SAGE_MODEL_PREFIX
        if hasattr(settings, "SAGE_MODEL_TEMPLATE"):
            del settings.SAGE_MODEL_TEMPLATE

        errors = check_required_settings(None)
        assert len(errors) == 2
        assert errors[0].id == "sage_invoice.E003"
        assert (
            errors[0].msg == "The required setting 'SAGE_MODEL_PREFIX' is not defined."
        )
        assert errors[1].id == "sage_invoice.E004"
        assert (
            errors[1].msg
            == "The required setting 'SAGE_MODEL_TEMPLATE' is not defined."
        )
