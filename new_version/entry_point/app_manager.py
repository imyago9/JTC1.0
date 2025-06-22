import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication

from entry_point.login_components.login_gui import LoginGUI
from main_gui.jt_gui import JournalTradeGUI


class AppManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("JournalTrade")

        # Create windows once
        self.login_window = LoginGUI()
        self.main_window = JournalTradeGUI()

        # Wire signals
        self.login_window.login_successful.connect(self.show_main)
        self.main_window.logout_requested.connect(self.show_login)

    # ---------- utility ---------- #
    @staticmethod
    def _center_on_primary(widget):
        """Place `widget` at the centre of the primary screen."""
        geom = widget.frameGeometry()
        center = QGuiApplication.primaryScreen().availableGeometry().center()
        geom.moveCenter(center)
        widget.move(geom.topLeft())

    # ────────────────── state transitions ──────────────────
    def show_login(self):
        # record where the main window was, if visible
        if self.main_window.isVisible():
            self._last_geometry = self.main_window.frameGeometry()

        self.main_window.hide()

        # decide where to place the login window
        if self._last_geometry:
            self.login_window.move(self._last_geometry.topLeft())
        else:
            self._center_on_primary(self.login_window)

        self.login_window.show()

    def show_main(self):
        # record where the login window was, if visible
        if self.login_window.isVisible():
            self._last_geometry = self.login_window.frameGeometry()

        self.login_window.hide()

        # use last geometry or centre
        if self._last_geometry:
            self.main_window.move(self._last_geometry.topLeft())
        else:
            self._center_on_primary(self.main_window)

        self.main_window.show()

    # ────────────────── entry point ──────────────────
    def run(self):
        self.login_window.show()
        self._center_on_primary(self.login_window)
        sys.exit(self.app.exec_())
