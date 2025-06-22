from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QWidget
from old_version.utils import error_catcher
import logging


class LoginView(QWidget):
    b_pressed_forgot_pass = pyqtSignal()
    b_pressed_login = pyqtSignal(object, object)
    b_pressed_register = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_input = None
        self.username_input = None

        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        button_forgot_password = QPushButton('Forgot Password')
        button_login = QPushButton('Login')
        button_register = QPushButton('Register')
        layout.addStretch()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button_forgot_password)
        layout.addStretch()
        layout.addWidget(button_login)
        layout.addWidget(button_register)
        self.setLayout(layout)

        button_forgot_password.setObjectName('LV_button_forgot_password')
        button_login.setObjectName('LV_button_login')
        button_register.setObjectName('LV_button_register')

        self.username_input.returnPressed.connect(button_login.click)
        self.password_input.returnPressed.connect(button_login.click)

        button_forgot_password.clicked.connect(self.button_pressed_forgot_password)
        button_login.clicked.connect(self.button_pressed_login)
        button_register.clicked.connect(self.button_pressed_register)

    def lv_reset_text(self):
        self.username_input.setPlaceholderText('Username')
        self.username_input.clear()
        self.username_input.setFocus()

        self.password_input.setPlaceholderText('Password')
        self.password_input.clear()
        self.username_input.setText('yago')
        self.password_input.setText('YYY123')

    def button_pressed_forgot_password(self):
        self.b_pressed_forgot_pass.emit()

    def button_pressed_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.b_pressed_login.emit(username, password)

    def button_pressed_register(self):
        self.b_pressed_register.emit()



