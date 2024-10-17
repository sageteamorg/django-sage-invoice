from rest_framework.exceptions import NotFound
from rest_framework.versioning import BaseVersioning

SUPPORTED_VERSIONS = ["1.0"]


class HeaderVersioning(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        # Get the version from the 'X-API-Version' header
        accept_header = request.META.get("HTTP_X_API_VERSION", "")

        # Check if the version header contains 'v'
        if "v" in accept_header:
            version = accept_header.split("v")[-1].split("+")[0]
        else:
            version = None

        # If no version is found, default to the latest version
        if not version:
            return SUPPORTED_VERSIONS[-1]  # Latest version

        # If version is not supported, raise an error
        if version not in SUPPORTED_VERSIONS:
            raise NotFound(f"API version '{version}' is not supported.")

        return version
