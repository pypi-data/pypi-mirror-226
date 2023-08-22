"""
# Purpose

Provide access to version information as well as dependencies

# Usage example


```python
import ewslib_core.ews_env

print(ewslib_core.ews_env.version_info())
```

# Tests

See [tests](site:tests/test_version).

"""

__all__ = ("VERSION", "version_info")

VERSION = "0.1.1"


def version_info() -> str:
    """
    Show the version info

    Example:
        ```python
        import ewslib_core.ews_env

        print(ewslib_core.ews_env.version_info())
        ```

    """
    import platform
    import sys
    from importlib import import_module  # noqa: F401
    from pathlib import Path

    optional_deps = []

    info = {
        "ewslib_core.ews_env version": VERSION,
        "install path": Path(__file__).resolve().parent,
        "python version": sys.version,
        "platform": platform.platform(),
        "optional deps. installed": optional_deps,
    }
    return "\n".join("{:>30} {}".format(k + ":", str(v).replace("\n", " ")) for k, v in info.items())
