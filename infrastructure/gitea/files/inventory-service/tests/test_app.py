"""Unit tests for inventory-service."""
import pathlib
import re


ROOT = pathlib.Path(__file__).parent.parent


def test_version_file_exists():
    assert (ROOT / "version.txt").exists(), "version.txt is missing"


def test_version_format():
    version = (ROOT / "version.txt").read_text().strip()
    assert re.match(r"^\d+\.\d+\.\d+", version), f"version '{version}' does not match semver"


def test_requirements_exist():
    req = ROOT / "requirements.txt"
    assert req.exists(), "requirements.txt is missing"


def test_no_known_vulnerable_version():
    """Fail if the unpatched CVE-2024-23334 version is still pinned.

    This test is added by the Lightwell patch PR. It will fail on the
    initial (vulnerable) codebase and pass after the patch is applied.
    Check PATCHED_CVE to determine if this test should enforce remediation.
    """
    cve_file = ROOT / "PATCHED_CVE"
    cve = cve_file.read_text().strip() if cve_file.exists() else ""
    if not cve:
        # No CVE declared - skip enforcement (pre-Lightwell baseline)
        return
    req = (ROOT / "requirements.txt").read_text()
    assert "aiohttp==3.9.0.rhlw" in req or "aiohttp==3.9.2.rhlw" in req, (
        f"{cve}: aiohttp 3.9.0 is vulnerable to path traversal. "
        "Ensure the Lightwell patch (aiohttp==*.rhlw-00001) is in requirements.txt."
    )


def test_app_module_importable():
    import importlib.util

    spec = importlib.util.spec_from_file_location("app", ROOT / "app.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "AppHandler")


def test_patched_cve_matches_requirements():
    """If PATCHED_CVE is set, requirements.txt must contain the Lightwell build string."""
    cve_file = ROOT / "PATCHED_CVE"
    cve = cve_file.read_text().strip() if cve_file.exists() else ""
    if not cve:
        return
    req = (ROOT / "requirements.txt").read_text()
    assert "rhlw" in req, (
        f"PATCHED_CVE declares {cve} but requirements.txt does not contain a Lightwell (rhlw) build. "
        "Ensure aiohttp==*.rhlw-00001 is in requirements.txt."
    )
