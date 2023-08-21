import os

__all__ = ["__version__"]

# Get the version from the VERSION file
# The VERSION file may be in the current directory or (in dev) one directory up

try:
    with open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "VERSION"),
        "r",
        encoding="utf-8",
    ) as version_file:
        __version__ = version_file.read().strip()

except IOError:
    try:
        with open(
            os.path.join(
                os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "VERSION"
            ),
            "r",
            encoding="utf-8",
        ) as version_file:
            __version__ = version_file.read().strip()
    except IOError:
        __version__ = "dev"
