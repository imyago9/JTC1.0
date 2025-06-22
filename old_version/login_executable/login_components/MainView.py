import logging
import sys
from enum import Enum

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtCore import Qt
from old_version.login_executable.login_components.bottom_frame.ForgotPassView import ForgotPassView
from old_version.login_executable.login_components.bottom_frame.LoginView import LoginView
from old_version.login_executable.login_components.bottom_frame.NewPasswordView import NewPasswordView
from old_version.login_executable.login_components.bottom_frame.RegisterView import RegisterView
from old_version.login_executable.login_components.bottom_frame.TwoFactorAuthView import TwoFactorAuthView
from old_version.utils import ResizableWindow, error_catcher
from old_version.login_executable.login_components.MainViewModel import LoginViewModel as LoginViewModel


class ViewStates(Enum):
    LOGIN = 0
    REGISTER = 1
    FORGOT_PASS = 2
    TWO_FACTOR_AUTH = 3
    NEW_PASSWORD = 4


class LoginWindowView(ResizableWindow):
    def __init__(self):
        super().__init__(hv='V')
        self.view_model = self.init_vm()
        self.view_state = None

        self.views = None
        self.bottom_view_stack = None

        self.setWindowTitle('JournalTrade Login Window')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        self.init_top_frame()
        self.init_bottom_frame()
        self.init_button_connections()

        self.display_login_view()

    @error_catcher(log_func=logging.error)
    def init_top_frame(self):
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        close_button = QPushButton(clicked=sys.exit)
        close_button.setObjectName('close_button')
        close_button.setIcon(self.view_model.get_icon('close_icon'))
        minimize_button = QPushButton(clicked=self.showMinimized)
        minimize_button.setObjectName('minimize_button')
        minimize_button.setIcon(self.view_model.get_icon('minimize_icon'))
        button_layout.addWidget(close_button)
        button_layout.addWidget(minimize_button)

        logo_label = QLabel()
        logo_label.setObjectName('logo_label')
        icon = self.view_model.get_icon('jt_logo_full')
        pixmap = icon.pixmap(icon.availableSizes()[0])
        logo_label.setPixmap(pixmap)
        layout.addLayout(button_layout)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        self.layout.addLayout(layout)

    @error_catcher(log_func=logging.error)
    def init_bottom_frame(self):
        self.bottom_view_stack = QStackedWidget()
        self.bottom_view_stack.setObjectName('bottom_view_stack')

        self.views = {'login_view': LoginView(),
                      'register_view': RegisterView(),
                      'forgot_pass_view': ForgotPassView(),
                      'two_factor_auth_view': TwoFactorAuthView(),
                      'new_password_view': NewPasswordView()}

        for view in [self.views['login_view'],
                     self.views['register_view'],
                     self.views['forgot_pass_view'],
                     self.views['two_factor_auth_view'],
                     self.views['new_password_view']]:
            self.bottom_view_stack.addWidget(view)
        self.layout.addWidget(self.bottom_view_stack)

    @error_catcher(log_func=logging.error)
    def init_button_connections(self):
        # LOGIN VIEW CONNECTIONS
        self.views['login_view'].b_pressed_forgot_pass.connect(self.display_forgot_pass_view)
        self.views['login_view'].b_pressed_login.connect(self.view_model.handle_lv_button_pressed_login)
        self.views['login_view'].b_pressed_register.connect(self.display_registration_view)
        # REGISTER VIEW CONNECTIONS
        self.views['register_view'].b_pressed_create_account.connect(
            self.view_model.handle_rv_button_pressed_create_account)
        self.views['register_view'].b_pressed_go_back.connect(self.display_login_view)
        # FORGOT PASSWORD VIEW CONNECTIONS
        self.views['forgot_pass_view'].b_pressed_submit_email.connect(
            self.view_model.handle_fpv_button_pressed_submit_email)
        self.views['forgot_pass_view'].b_pressed_go_back.connect(self.display_login_view)
        # NEW PASSWORD VIEW CONNECTIONS
        self.views['new_password_view'].b_pressed_submit_new_password.connect(self.view_model.verify_npv_otp)
        self.views['new_password_view'].b_pressed_go_back.connect(self.display_login_view)
        # TWO FACTOR AUTH VIEW CONNECTIONS
        self.views['two_factor_auth_view'].b_pressed_submit_otp.connect(self.view_model.verify_rv_otp)
        self.views['two_factor_auth_view'].b_pressed_go_back.connect(self.display_registration_view)
        # VIEW MODEL CONNECTIONS
        self.view_model.RV_otp_validated.connect(self.display_login_view)
        self.view_model.NPV_otp_validated.connect(self.display_login_view)
        self.view_model.handle_b_pressed_create_account.connect(self.display_two_factor_auth_view)
        self.view_model.handle_b_pressed_submit_email.connect(self.display_new_password_view)

    @error_catcher(log_func=logging.error)
    def display_login_view(self):
        if not self.view_state == ViewStates.LOGIN:
            self.view_state = ViewStates.LOGIN
            self.bottom_view_stack.setCurrentWidget(self.views['login_view'])
            self.views['login_view'].lv_reset_text()

    @error_catcher(log_func=logging.error)
    def display_registration_view(self):
        if not self.view_state == ViewStates.REGISTER:
            self.view_state = ViewStates.REGISTER
            self.bottom_view_stack.setCurrentWidget(self.views['register_view'])
            self.views['register_view'].rv_reset_text()

    @error_catcher(log_func=logging.error)
    def display_forgot_pass_view(self):
        if not self.view_state == ViewStates.FORGOT_PASS:
            self.view_state = ViewStates.FORGOT_PASS
            self.bottom_view_stack.setCurrentWidget(self.views['forgot_pass_view'])
            self.views['forgot_pass_view'].fpv_reset_text()

    @error_catcher(log_func=logging.error)
    def display_two_factor_auth_view(self):
        if not self.view_state == ViewStates.TWO_FACTOR_AUTH:
            self.view_state = ViewStates.TWO_FACTOR_AUTH
            self.bottom_view_stack.setCurrentWidget(self.views['two_factor_auth_view'])

    @error_catcher(log_func=logging.error)
    def display_new_password_view(self):
        if not self.view_state == ViewStates.NEW_PASSWORD:
            self.view_state = ViewStates.NEW_PASSWORD
            self.bottom_view_stack.setCurrentWidget(self.views['new_password_view'])

    @error_catcher(log_func=logging.error)
    def init_vm(self):
        view_model = LoginViewModel(self)
        view_model.init_style_sheet(self)
        return view_model
