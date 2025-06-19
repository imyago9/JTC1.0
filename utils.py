import sys
import os
import logging
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDesktopWidget, QMainWindow, QHBoxLayout, QDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt, QRect, QPoint


def error_catcher(log_func=None, default_return=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_message = f"Error in {func.__name__}: {e}"
                if log_func:
                    log_func(log_message)
                else:
                    logging.error(log_message)
                return default_return
        return wrapper
    return decorator


@error_catcher(log_func=logging.error, default_return=False)
def resource_path(relative_path):
    """
    Constructs the absolute path to a resource, accounting for PyInstaller bundling.
    """
    try:
        base_path = sys._MEIPASS  # Temp folder created by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(f"..")  # Base directory during development
    return os.path.join(base_path, relative_path)


def center_window(self):
    frame_geometry = self.frameGeometry()
    screen_center = QDesktopWidget().availableGeometry().center()
    frame_geometry.moveCenter(screen_center)
    self.move(frame_geometry.topLeft())


@error_catcher(log_func=logging.error, default_return=False)
def load_stylesheet(self, file_name):
    with open(resource_path(f'resources/styles/{file_name}.qss'), "r") as file:
        self.setStyleSheet(file.read())


class ResourceLoader:
    _icon_cache = {}  # Cache to store loaded icons

    @classmethod
    def get_icon(cls, name):
        """
        Retrieves an icon from the resources/icons folder, caching it for performance.
        """
        # Check if the icon is already in the cache
        if name in cls._icon_cache:
            return cls._icon_cache[name]

        # Construct the full path to the icon
        icon_dir = resource_path("resources/icons")
        icon_path = os.path.join(icon_dir, f"{name}.png")
        if os.path.exists(icon_path):
            try:
                icon = QtGui.QIcon(icon_path)
                cls._icon_cache[name] = icon  # Cache the loaded icon
                return icon
            except Exception as e:
                raise RuntimeError(f"Error loading icon '{name}': {e}")
        else:
            raise FileNotFoundError(f"Icon '{name}' not found in {icon_dir}")


class ResizableWindow(QMainWindow):
    def __init__(self, hv='V'):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create and set central widget
        central_widget = QWidget(self)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)
        # Add layout to the central widget
        self.layout = QVBoxLayout(central_widget) if hv == 'V' else QHBoxLayout(central_widget)
        central_widget.setLayout(self.layout)

        self.setWindowFlags(Qt.FramelessWindowHint)  # Frameless
        self.setMouseTracking(True)  # Enable mouse tracking
        self.resize_margin = 5  # Margin for resizing detection
        self.resizing = None
        self.mouse_pos = None
        self.rect_before_resize = None
        self._is_dragging = False
        self._drag_start_position = QPoint()

    def get_resize_direction(self, pos):
        try:
            """
            Detect which edge or corner is being hovered for resizing.
            """
            rect = self.rect()
            if pos.x() <= self.resize_margin:
                if pos.y() <= self.resize_margin:
                    return 'top_left'
                elif pos.y() >= rect.height() - self.resize_margin:
                    return 'bottom_left'
                else:
                    return 'left'
            elif pos.x() >= rect.width() - self.resize_margin:
                if pos.y() <= self.resize_margin:
                    return 'top_right'
                elif pos.y() >= rect.height() - self.resize_margin:
                    return 'bottom_right'
                else:
                    return 'right'
            elif pos.y() <= self.resize_margin:
                return 'top'
            elif pos.y() >= rect.height() - self.resize_margin:
                return 'bottom'
            return None
        except Exception as e:
            print(f"Error in get_resize_direction: {e}")

    def resize_window(self, global_pos):
        try:
            """
            Resize the window based on the resize direction and mouse movement.
            """
            delta = global_pos - self.mouse_pos
            rect = self.rect_before_resize

            if self.resizing == 'left':
                new_rect = QRect(rect.left() + delta.x(), rect.top(), rect.width() - delta.x(), rect.height())
            elif self.resizing == 'right':
                new_rect = QRect(rect.left(), rect.top(), rect.width() + delta.x(), rect.height())
            elif self.resizing == 'top':
                new_rect = QRect(rect.left(), rect.top() + delta.y(), rect.width(), rect.height() - delta.y())
            elif self.resizing == 'bottom':
                new_rect = QRect(rect.left(), rect.top(), rect.width(), rect.height() + delta.y())
            elif self.resizing == 'top_left':
                new_rect = QRect(rect.left() + delta.x(), rect.top() + delta.y(), rect.width() - delta.x(), rect.height() - delta.y())
            elif self.resizing == 'top_right':
                new_rect = QRect(rect.left(), rect.top() + delta.y(), rect.width() + delta.x(), rect.height() - delta.y())
            elif self.resizing == 'bottom_left':
                new_rect = QRect(rect.left() + delta.x(), rect.top(), rect.width() - delta.x(), rect.height() + delta.y())
            elif self.resizing == 'bottom_right':
                new_rect = QRect(rect.left(), rect.top(), rect.width() + delta.x(), rect.height() + delta.y())

            # Apply constraints for minimum width and height
            if new_rect.width() >= self.minimumWidth() and new_rect.height() >= self.minimumHeight():
                self.setGeometry(new_rect)
        except Exception as e:
            print(f"Error in resize_window: {e}")

    def mousePressEvent(self, event):
        try:
            """
            Start resizing or dragging based on mouse position.
            """
            if event.button() == Qt.LeftButton:
                resize_direction = self.get_resize_direction(event.pos())
                if resize_direction:
                    self.resizing = resize_direction
                    self.mouse_pos = event.globalPos()
                    self.rect_before_resize = self.geometry()
                else:
                    self.resizing = None
                    self._is_dragging = True
                    self._drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
        except Exception as e:
            print(f"Error in mousePressEvent: {e}")

    def mouseMoveEvent(self, event):
        try:
            """
            Handle resizing or dragging while moving the mouse.
            """
            if self.resizing:
                self.resize_window(event.globalPos())
            elif self._is_dragging:
                self.move(event.globalPos() - self._drag_start_position)
                event.accept()
            else:
                # Update cursor shape based on resize direction
                resize_direction = self.get_resize_direction(event.pos())
                if resize_direction in ('top', 'bottom'):
                    self.setCursor(Qt.SizeVerCursor)
                elif resize_direction in ('left', 'right'):
                    self.setCursor(Qt.SizeHorCursor)
                elif resize_direction in ('top_left', 'bottom_right'):
                    self.setCursor(Qt.SizeFDiagCursor)
                elif resize_direction in ('top_right', 'bottom_left'):
                    self.setCursor(Qt.SizeBDiagCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
        except  Exception as e:
            print(f"Error in mouseMoveEvent: {e}")

    def mouseReleaseEvent(self, event):
        try:
            """
            Reset resizing and dragging states on mouse release.
            """
            if event.button() == Qt.LeftButton:
                self.resizing = None
                self._is_dragging = False
                self.setCursor(Qt.ArrowCursor)
                event.accept()
        except Exception as e:
            print(f"Error in mouseReleaseEvent: {e}")


def show_message(self, title, message):
    try:
        msg_box = ErrorPopup(self, title, message)
        msg_box.exec_()
        msg_box.center_to_parent()
    except Exception as e:
        logging.error(f"Error showing message: {e}")


class ErrorPopup(QDialog):

    def __init__(self, parent=None, title='Error', text='An error occurred.'):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setStyleSheet("border-radius: 7px; border: 2px solid #e0a3a3; color: white; background-color: #2b2b2b;")

        self.layout = QVBoxLayout()

        label = QLabel(text)
        label.setStyleSheet('border: none;')
        button = QPushButton('OK', clicked=self.close)  # type: ignore
        button.setStyleSheet('background-color: #e0a3a3; color: black; border: none;')
        self.layout.addWidget(label)
        self.layout.addWidget(button)
        self.setLayout(self.layout)

    def center_to_parent(self):
        """Centers the dialog relative to its parent."""
        if self.parent():
            print(self.parent())
            parent_geometry = self.parent().geometry()
            self_geometry = self.geometry()

            # Calculate the new position
            x = parent_geometry.x() + (parent_geometry.width() - self_geometry.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self_geometry.height()) // 2

            # Move the dialog to the calculated position
            self.move(x, y)


