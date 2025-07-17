import os
import sys
import logging
from PyQt5 import QtGui


def resource_path(relative_path: str) -> str:
    """Return absolute path to resource, works for dev and for PyInstaller."""
    try:
            base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
    return os.path.join(base_path, relative_path)


def load_stylesheet(widget, name: str) -> None:
    """Load a .qss stylesheet from resources/styles and apply to widget."""
    path = resource_path(os.path.join("resources", "styles", f"{name}.qss"))
    try:
            with open(path, "r") as f:
                widget.setStyleSheet(f.read())
    except Exception as e:
        logging.error(f"Failed to load stylesheet '{name}': {e}")


class ResourceLoader:
    """Helper class to retrieve icons from resources/icons with caching."""
    _icon_cache: dict = {}

    @classmethod
    def get_icon(cls, name: str) -> QtGui.QIcon:
        if name in cls._icon_cache:
            return cls._icon_cache[name]

        path = resource_path(os.path.join("resources", "icons", f"{name}.png"))
        if not os.path.exists(path):
            raise FileNotFoundError(f"Icon '{name}' not found at {path}")
        try:
            icon = QtGui.QIcon(path)
            cls._icon_cache[name] = icon
            return icon
        except Exception as e:
            raise RuntimeError(f"Error loading icon '{name}': {e}")
