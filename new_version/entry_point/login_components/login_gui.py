import logging
import sys
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QPainter, QPalette, QBrush, QColor, QPainterPath, QRegion
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget
from custom_widgets.custom_widgets import CustomFrameWindow
from PyQt5.QtCore import Qt, pyqtSignal, QRectF

from entry_point.login_components.login_components import LoginView, RegisterView, NewPasswordView, ForgotPassView, TwoFactorAuthView
from utils import ResourceLoader

class ViewStates(Enum):
    LOGIN = 0
    REGISTER = 1
    FORGOT_PASS = 2
    TWO_FACTOR_AUTH = 3
    NEW_PASSWORD = 4

class LoginGUI(CustomFrameWindow):
    login_successful = pyqtSignal()
    def __init__(self):
        super().__init__(hv='V')
        self.setWindowTitle('JournalTrade Login Window')
        self.setObjectName('LoginGUI')

        self._bg_orig = ResourceLoader.get_background("login_landscape")
        self.RADIUS = 9

        self._build_ui()
        self._wire_buttons()

    # ────────────────────────── Background Image ─────────────────────────────
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_round_mask()
        self._apply_background()

    def _apply_round_mask(self):
        path  = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.RADIUS, self.RADIUS)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def _apply_background(self):
        if self.width() == 0 or self.height() == 0:
            return
        scaled = self._bg_orig.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation) # type: ignore
        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(scaled)) # type: ignore
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    # ────────────────────────── UI BUILDER ─────────────────────────────
    def _build_ui(self):
        self._setup_top_frame()
        self._setup_bottom_frame()

    # ────────────────────────── Top Frame ─────────────────────────────
    def _setup_top_frame(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        close_button = QPushButton(clicked=sys.exit, objectName='close_button', icon=ResourceLoader.get_icon("close_window"), toolTip='Close app.', cursor=Qt.PointingHandCursor) # type: ignore
        minimize_button = QPushButton(clicked=self.showMinimized, objectName='minimize_button', icon=ResourceLoader.get_icon("minimize_window"), cursor=Qt.PointingHandCursor) # type: ignore
        button_layout.addWidget(QLabel('JournalTrade by Y', objectName='signature_label')) # type: ignore
        button_layout.addStretch()
        button_layout.addWidget(minimize_button)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.layout.addLayout(layout)
        self.enable_title_bar_drag(int(close_button.sizeHint().height()*3))

    # ────────────────────────── Bottom Frame ─────────────────────────────
    def _setup_bottom_frame(self):
        self.stack = QStackedWidget()
        self.stack.setObjectName('lg_bvs')
        # Dynamically load all views
        self.views = {
            ViewStates.LOGIN: LoginView(),
            ViewStates.REGISTER: RegisterView(),
            ViewStates.FORGOT_PASS: ForgotPassView(),
            ViewStates.TWO_FACTOR_AUTH: TwoFactorAuthView(),
            ViewStates.NEW_PASSWORD: NewPasswordView()
        }
        for v in self.views.values():
            self.stack.addWidget(v)
        self.layout.addWidget(self.stack)
        self.set_view(ViewStates.LOGIN)

    # ─────────────────── Wiring Buttons and Signals ────────────────────
    def _wire_buttons(self):
        v = self.views
        s = ViewStates
        # ╭─ LoginView Connections ────────────────────╮
        v[s.LOGIN].pressed_forgot_pass.connect(lambda: self.set_view(s.FORGOT_PASS))
        v[s.LOGIN].pressed_login.connect(self.login_successful.emit)
        v[s.LOGIN].pressed_register.connect(lambda: self.set_view(s.REGISTER))
        # ╭─ RegisterView Connections ─────────────────╮
        v[s.REGISTER].pressed_back.connect(lambda: self.set_view(s.LOGIN))
        # ╭─ ForgotPassView Connections ───────────────╮
        v[s.FORGOT_PASS].pressed_back.connect(lambda: self.set_view(s.LOGIN))
        # ╭─ NewPasswordView Connections ──────────────╮
        v[s.NEW_PASSWORD].pressed_back.connect(lambda: self.set_view(s.LOGIN))
        # ╭─ Two-Factor Auth View Connections ─────────╮
        v[ViewStates.TWO_FACTOR_AUTH].pressed_back.connect(lambda: self.set_view(s.REGISTER))

    # ──────────────────────── Swap Across ViewStates ─────────────────────
    def set_view(self, state: ViewStates):
        if getattr(self, '_state', None) == state:
            return
        self._state = state
        self.stack.setCurrentWidget(self.views[state])
        reset = getattr(self.views[state], f'{state.name.lower()}_reset_text', None)
        if callable(reset):
            reset()


