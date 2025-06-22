from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout


class CustomFrameWindow(QMainWindow):
    def __init__(self, hv='V'):
        super().__init__()
        self.setObjectName("MainWindow")

        central_widget = QWidget(self)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget) if hv == 'V' else QHBoxLayout(central_widget)
        central_widget.setLayout(self.layout)

        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.resize_margin = 5
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
