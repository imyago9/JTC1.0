import logging
import sys
from enum import Enum

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal
from custom_widgets.custom_widgets import CustomFrameWindow
"""from login_executable.login_components.bottom_frame.ForgotPassView import ForgotPassView
from login_executable.login_components.bottom_frame.LoginView import LoginView
from login_executable.login_components.bottom_frame.NewPasswordView import NewPasswordView
from login_executable.login_components.bottom_frame.RegisterView import RegisterView
from login_executable.login_components.bottom_frame.TwoFactorAuthView import TwoFactorAuthView
from login_executable.login_components.MainViewModel import LoginViewModel as LoginViewModel"""

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

class LoginGUI(CustomFrameWindow):
    login_successful = pyqtSignal()
    def __init__(self):
        super().__init__(hv='V')
        self.setWindowTitle('JournalTrade Login Window')

        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        self.init_top_frame()
        self.init_bottom_frame()

    @error_catcher(log_func=logging.error)
    def init_top_frame(self):

        button_layout = QHBoxLayout()
        close_button = QPushButton(clicked=sys.exit)
        minimize_button = QPushButton(clicked=self.showMinimized)
        button_layout.addWidget(close_button)
        button_layout.addWidget(minimize_button)

        self.layout.addLayout(button_layout)

    @error_catcher(log_func=logging.error)
    def init_bottom_frame(self):
        self.bottom_view_stack = QStackedWidget()
        btn = QPushButton('Log in')
        btn.clicked.connect(self.login_successful.emit)
        self.bottom_view_stack.addWidget(btn)
        self.layout.addWidget(self.bottom_view_stack)

