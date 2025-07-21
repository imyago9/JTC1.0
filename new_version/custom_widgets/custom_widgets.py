from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout


class CustomFrameWindow(QMainWindow):
    def __init__(self, hv='V'):
        super().__init__()
        self.setObjectName("MainWindow")
        self.hv = hv  # 'V' for vertical, 'H' for horizontal
        central_widget = QWidget(self)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget) if hv == 'V' else QHBoxLayout(central_widget)
        central_widget.setLayout(self.layout)
        self.setWindowFlags(Qt.FramelessWindowHint) # type: ignore
        self._title_bar_height = 0
        self._allow_dblclk_max = False
        self._drag_offset     = None
        self._is_maximized    = False

        # public helper for children
    def enable_title_bar_drag(self,
                              title_bar_height: int,
                              allow_double_click_max=False):
        """Call once after your title bar is laid out."""
        self._title_bar_height = title_bar_height
        self._allow_dblclk_max = allow_double_click_max
    # mouse events
    def mousePressEvent(self, event):
        try:
            if (event.button() == Qt.LeftButton
                    and event.pos().y() <= self._title_bar_height):
                self._drag_offset = (event.globalPos()
                                     - self.frameGeometry().topLeft())
            else:
                self._drag_offset = None
            super().mousePressEvent(event)
        except Exception as e:
            print(f"Error in mousePressEvent: {e}")

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() & Qt.LeftButton and self._drag_offset:
                # if a subclass has a restore routine, call it once
                if getattr(self, "_is_maximized", False):
                    ratio_x = event.x() / self.width()
                    if hasattr(self, "_toggle_max_restore"):
                        self._toggle_max_restore()
                    new_x = int(event.globalX() - ratio_x * self.width())
                    new_y = max(event.globalY() - 15, 0)
                    self.move(new_x, new_y)
                    self._drag_offset = (event.globalPos()
                                         - self.frameGeometry().topLeft())
                else:
                    self.move(event.globalPos() - self._drag_offset)
            super().mouseMoveEvent(event)
        except Exception as e:
            print(f"Error in mouseMoveEvent: {e}")

    def mouseReleaseEvent(self, event):
        self._drag_offset = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if (self._allow_dblclk_max
                and event.button() == Qt.LeftButton
                and event.pos().y() <= self._title_bar_height
                and hasattr(self, "_toggle_max_restore")):
            self._toggle_max_restore()
            return
        super().mouseDoubleClickEvent(event)
