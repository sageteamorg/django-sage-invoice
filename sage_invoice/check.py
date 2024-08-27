from importlib.util import find_spec

from django.conf import settings
from django.core.checks import Error, register


@register()
def check_installed_apps(app_configs, **kwargs):
    errors = []
    required_apps = [
        "sage_invoice",
    ]

    for app in required_apps:
        if app not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    f"'{app}' is missing in INSTALLED_APPS.",
                    hint=f"Add '{app}' to INSTALLED_APPS in your settings.",
                    obj=settings,
                    id=f"sage_invoice.E00{required_apps.index(app) + 1}",
                )
            )

    return errors


@register()
def check_required_libraries(app_configs, **kwargs):
    errors = []
    required_libraries = [
        "sage_invoice",
    ]

    for library in required_libraries:
        if not find_spec(library):
            errors.append(
                Error(
                    f"The required library '{library}' is not installed.",
                    hint=f"Install '{library}' via pip: pip install {library}",
                    obj=settings,
                    id=f"sage_invoice.E00{required_libraries.index(library) + 2}",
                )
            )

    return errors


@register()
def check_required_settings(app_configs, **kwargs):
    errors = []

    required_settings = [
        "MODEL_PREFIX",
        "MODEL_TEMPLATE",
    ]

    for setting in required_settings:
        if not hasattr(settings, setting):
            errors.append(
                Error(
                    f"The required setting '{setting}' is not defined.",
                    hint=f"Define '{setting}' in your settings.py.",
                    obj=settings,
                    id=f"sage_invoice.E00{required_settings.index(setting) + 3}",
                )
            )
    return errors
