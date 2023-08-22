"""
Test suite for the module [test_lib.version](site:api/test_lib/version).
"""

import re

from packaging.version import (
    parse as parse_version,  # pyright: ignore [reportMissingImports]
)

import ewslib_core.ews_env


def test_version_info():
    """Test the version_info"""
    s = ewslib_core.ews_env.version_info()
    assert re.match(" *ewslib_core.ews_env version: ", s)
    assert s.count("\n") == 4  # noqa: PLR2004


def test_standard_version():
    """Test the standard version"""
    v = parse_version(ewslib_core.ews_env.VERSION)
    assert str(v) == ewslib_core.ews_env.VERSION


def test_version_attribute_is_present():
    """Test that __version__ is present"""
    assert hasattr(ewslib_core.ews_env, "__version__")


def test_version_attribute_is_a_string():
    """Test that __version__ is a string"""
    assert isinstance(ewslib_core.ews_env.__version__, str)
