import logging
import sys
from enum import Enum

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QStackedWidget
from custom_widgets.custom_widgets import CustomFrameWindow
from PyQt5.QtCore import Qt, pyqtSignal

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
        #init variables
        self.views = None
        self.view_state = None
        self.bottom_view_stack = None
        self.setWindowTitle('JournalTrade Login Window')

        self.init_gui()

    def init_gui(self):
        self.init_top_frame()
        self.init_bottom_frame()
        self.wire_button_connections()

    def init_top_frame(self):
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        close_button = QPushButton(clicked=sys.exit)
        close_button.clicked.connect(sys.exit)
        close_button.setObjectName('close_button')
        close_button.setIcon(ResourceLoader.get_icon("close_window"))
        minimize_button = QPushButton(clicked=self.showMinimized)
        minimize_button.setObjectName('minimize_button')
        minimize_button.setIcon(ResourceLoader.get_icon("minimize_window"))
        button_layout.addWidget(close_button)
        button_layout.addWidget(minimize_button)

        """logo_label = QLabel()
        logo_label.setObjectName('logo_label')
        icon = ResourceLoader.get_icon('jt_logo_full')
        pixmap = icon.pixmap(icon.availableSizes()[0])
        logo_label.setPixmap(pixmap)""" # Working on logo

        layout.addLayout(button_layout)
        # layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        self.layout.addLayout(layout)

    def init_bottom_frame(self):
        self.bottom_view_stack = QStackedWidget()
        self.bottom_view_stack.setObjectName('lg_bvs')
        self.views = {'login_view': LoginView(),
                      'register_view': RegisterView(),
                      'forgot_pass_view': ForgotPassView(),
                      'two_factor_auth_view': TwoFactorAuthView(),
                      'new_password_view': NewPasswordView()}
        for view in self.views.values():
            self.bottom_view_stack.addWidget(view)
        self.display_login_view()
        self.layout.addWidget(self.bottom_view_stack)

    def wire_button_connections(self):
        self.views['login_view'].b_pressed_forgot_pass.connect(self.display_forgot_pass_view)
        self.views['login_view'].b_pressed_login.connect(self.login_successful.emit)
        self.views['login_view'].b_pressed_register.connect(self.display_registration_view)

        self.views['register_view'].b_pressed_go_back.connect(self.display_login_view)
        # self.views['register_view'].b_pressed_create_account.connect( BUILD )

        self.views['new_password_view'].b_pressed_go_back.connect(self.display_login_view)
        # self.views['new_password_view'].b_pressed_submit_new_password.connect( GOTTA BUILD )

        self.views['forgot_pass_view'].b_pressed_go_back.connect(self.display_login_view)
        # self.views['forgot_pass_view'].b_pressed_submit_email.connect( GOTTA BUILD )

        self.views['two_factor_auth_view'].b_pressed_go_back.connect(self.display_registration_view)
        self.views['two_factor_auth_view'].b_pressed_submit_otp.connect(self.view_model.verify_rv_otp)

    def display_login_view(self):
        if not self.view_state == ViewStates.LOGIN:
            self.view_state = ViewStates.LOGIN
            self.bottom_view_stack.setCurrentWidget(self.views['login_view'])
            self.views['login_view'].lv_reset_text()

    def display_registration_view(self):
        if not self.view_state == ViewStates.REGISTER:
            self.view_state = ViewStates.REGISTER
            self.bottom_view_stack.setCurrentWidget(self.views['register_view'])
            self.views['register_view'].rv_reset_text()

    def display_forgot_pass_view(self):
        if not self.view_state == ViewStates.FORGOT_PASS:
            self.view_state = ViewStates.FORGOT_PASS
            self.bottom_view_stack.setCurrentWidget(self.views['forgot_pass_view'])
            self.views['forgot_pass_view'].fpv_reset_text()

    def display_two_factor_auth_view(self):
        if not self.view_state == ViewStates.TWO_FACTOR_AUTH:
            self.view_state = ViewStates.TWO_FACTOR_AUTH
            self.bottom_view_stack.setCurrentWidget(self.views['two_factor_auth_view'])

    def display_new_password_view(self):
        if not self.view_state == ViewStates.NEW_PASSWORD:
            self.view_state = ViewStates.NEW_PASSWORD
            self.bottom_view_stack.setCurrentWidget(self.views['new_password_view'])

