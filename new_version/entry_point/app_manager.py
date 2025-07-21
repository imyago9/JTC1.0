import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication

from entry_point.login_components.login_gui import LoginGUI
from main_gui.jt_gui import JournalTradeGUI
from utils import load_stylesheet


class AppManager:
    def __init__(self):
        self._last_geometry_login = None
        self._last_geometry_main = None
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("JournalTrade")

        self.login_window = LoginGUI()
        self.main_window = JournalTradeGUI()

        load_stylesheet(self.login_window, 'login_window')
        load_stylesheet(self.main_window, 'main_window')

        self.login_window.login_successful.connect(self.show_main)
        self.main_window.logout_requested.connect(self.show_login)

    # ---------- window sizing utility ---------- #
    @staticmethod
    def _center_on_primary(widget):
        geom = widget.frameGeometry()
        center = QGuiApplication.primaryScreen().availableGeometry().center()
        geom.moveCenter(center)
        widget.move(geom.topLeft())

    @staticmethod
    def _resize_to_monitor(widget, x_scale, y_scale):
        screen = widget.screen().geometry()
        screen_width  = screen.width()
        screen_height = screen.height()
        window_width  = int(screen_width * x_scale)
        window_height = int(screen_height * y_scale)
        widget.resize(window_width, window_height)

    # ────────────────── state transitions ──────────────────
    def show_login(self):
        if self.main_window.isVisible():
            self._last_geometry_main = self.main_window.frameGeometry()
        self.main_window.hide()
        if self._last_geometry_login:
            self.login_window.move(self._last_geometry_login.topLeft())
        else:
            self._center_on_primary(self.login_window)
        self.login_window.show()

    def show_main(self):
        if self.login_window.isVisible():
            self._last_geometry_login = self.login_window.frameGeometry()
        self.login_window.hide()
        if self._last_geometry_main:
            self.main_window.move(self._last_geometry_main.topLeft())
        else:
            self._resize_to_monitor(self.main_window, 0.85, 0.75)
            self._center_on_primary(self.main_window)
        self.main_window.show()

    # ────────────────── entry point ──────────────────
    def run(self):
        self.login_window.show()
        self._center_on_primary(self.login_window)
        sys.exit(self.app.exec_())
