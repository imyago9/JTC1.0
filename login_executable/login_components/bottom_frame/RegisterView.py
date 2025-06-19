from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from utils import error_catcher
import logging


class RegisterView(QWidget):
    b_pressed_create_account = pyqtSignal(object, object, object, object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.email_input = None
        self.username_input = None
        self.password_input = None
        self.confirm_password_input = None
        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        layout = QVBoxLayout()
        self.email_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        button_create_account = QPushButton('Create Account')
        button_back_to_login = QPushButton('Back To Login')

        layout.addStretch()
        layout.addWidget(self.email_input)
        layout.addSpacing(5)
        layout.addWidget(self.username_input)
        layout.addSpacing(5)
        layout.addWidget(self.password_input)
        layout.addSpacing(3)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(5)
        layout.addWidget(button_create_account)
        layout.addWidget(button_back_to_login)
        self.setLayout(layout)

        button_create_account.clicked.connect(self.button_pressed_create_account)
        self.email_input.returnPressed.connect(button_create_account.click)
        self.username_input.returnPressed.connect(button_create_account.click)
        self.password_input.returnPressed.connect(button_create_account.click)
        self.confirm_password_input.returnPressed.connect(button_create_account.click)
        button_back_to_login.clicked.connect(self.button_pressed_go_back)

        self.email_input.setObjectName('RV_email_input')
        self.password_input.setObjectName('RV_password_input')
        self.confirm_password_input.setObjectName('RV_confirm_password_input')
        button_create_account.setObjectName('RV_button_create_account')
        button_back_to_login.setObjectName('RV_button_back_to_login')

    def rv_reset_text(self):
        self.email_input.setPlaceholderText('Email')
        self.email_input.clear()
        self.username_input.setPlaceholderText('Username')
        self.username_input.clear()
        self.password_input.setPlaceholderText('Password')
        self.password_input.clear()
        self.confirm_password_input.setPlaceholderText('Confirm Password')
        self.confirm_password_input.clear()
        self.email_input.setFocus()

    def button_pressed_create_account(self):
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        self.b_pressed_create_account.emit(email, username, password, confirm_password)

    def button_pressed_go_back(self):
        self.b_pressed_go_back.emit()
