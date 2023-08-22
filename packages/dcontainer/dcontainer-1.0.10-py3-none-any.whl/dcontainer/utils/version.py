import importlib
import json
import urllib
import urllib.request
from importlib.metadata import version
from typing import List

OWN_REPO = "devcontainers-contrib/dcontainer"
NANOLAYER_REPO = "devcontainers-contrib/nanolayer"
OWN_PACKAGE = "dcontainer"
NANOLAYER_PACKAGE = "nanolayer"


def _resolve_package_version(package: str) -> str:
    return version(package)


def _get_latest_release(repo: str) -> str:
    response = urllib.request.urlopen(
        f"https://api.github.com/repos/{repo}/releases/latest"
    )  # nosec
    response_json = json.loads(response.read())
    resolved_version = response_json["name"]
    return resolved_version


def _get_github_tags(repo: str) -> List[str]:
    response = urllib.request.urlopen(
        f"https://api.github.com/repos/{repo}/tags"
    )  # nosec
    return [tag["name"] for tag in json.loads(response.read())]


def resolve_own_package_version() -> str:
    return _resolve_package_version(OWN_PACKAGE)


def resolve_nanolayer_release_version() -> str:
    try:
        package_version = _resolve_package_version(NANOLAYER_PACKAGE)
    except importlib.metadata.PackageNotFoundError:
        package_version = None

    if package_version is not None:
        tags = _get_github_tags(NANOLAYER_REPO)
        if f"v{package_version}" in tags:
            return f"v{package_version}"

    return _get_latest_release(NANOLAYER_REPO)
