import os
import sys
import logging
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDate
from typing import Iterable
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsOpacityEffect, QLabel, QWidget


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
    _bg_cache: dict = {}

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

    @classmethod
    def get_background(cls, name: str) -> QtGui.QPixmap:
        """
        Returns a cached QPixmap for a background image located at
        resources/backgrounds/<name>login_landscape2.png
        """
        if name in cls._bg_cache:
            return cls._bg_cache[name]

        path = resource_path(os.path.join("resources", "backgrounds",
                                          f"{name}.png"))
        if not os.path.exists(path):
            raise FileNotFoundError(f"Background '{name}' not found at {path}")

        pixmap = QtGui.QPixmap(path)
        if pixmap.isNull():
            raise RuntimeError(f"Failed to load background '{name}' from {path}")

        cls._bg_cache[name] = pixmap
        return pixmap
def _make_layout(layout_cls, parent=None, margin: int = 10, spacing: int = 10):
    layout = layout_cls(parent)
    layout.setContentsMargins(margin, margin, margin, margin)
    layout.setSpacing(spacing)
    return layout


def vbox(parent=None, *, margin: int = 0, spacing: int = 0) -> QVBoxLayout:
    """Create a QVBoxLayout with uniform margins and spacing."""
    return _make_layout(QVBoxLayout, parent, margin, spacing)


def hbox(parent=None, *, margin: int = 0, spacing: int = 0) -> QHBoxLayout:
    """Create a QHBoxLayout with uniform margins and spacing."""
    return _make_layout(QHBoxLayout, parent, margin, spacing)


def grid(parent=None, *, margin: int = 0, spacing: int = 0) -> QGridLayout:
    """Create a QGridLayout with uniform margins and spacing."""
    return _make_layout(QGridLayout, parent, margin, spacing)

def translucent_label(pixmap, object_name, opacity=0.1):
    """Create a QLabel with a translucent pixmap."""
    lbl = QLabel(objectName=object_name) # type: ignore
    lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    lbl.setPixmap(pixmap)
    effect = QGraphicsOpacityEffect(lbl)
    effect.setOpacity(opacity)
    lbl.setGraphicsEffect(effect)
    return lbl

def change_opacity(widgets: Iterable[QWidget], opacity: float) -> None:
    """
    Apply a fade‑in/out effect to each widget in *sides*.

    Parameters
    ----------
    widgets: any iterable of QWidget
    opacity: 0.0 (fully transparent) … 1.0 (fully opaque)
    """
    for widget in widgets:
        if opacity >= 1:
            # Remove any effect and restore normal mouse events
            widget.setGraphicsEffect(None)
            widget.setAttribute(Qt.WA_TransparentForMouseEvents, False) # type: ignore
        else:
            eff = widget.graphicsEffect()
            if eff is None:
                eff = QGraphicsOpacityEffect(widget)
                widget.setGraphicsEffect(eff)
            eff.setOpacity(opacity)
            widget.setAttribute(Qt.WA_TransparentForMouseEvents, True) # type: ignore
        widget.update()

def mock_data(start: QDate, end: QDate, *, min_points: int = 30):
    import numpy as np, datetime as dt
    py_start = start.toPyDate()
    py_end   = end.toPyDate()

    n_days = (py_end - py_start).days + 1
    if n_days < min_points:
        py_start = py_end - dt.timedelta(days=min_points - 1)
        n_days   = min_points

    profits = np.random.normal(100, 20, n_days)
    data = [
        {"date": py_start + dt.timedelta(days=i),
         "profit": round(float(profits[i]), 2)}
        for i in range(n_days)
    ]
    return data
