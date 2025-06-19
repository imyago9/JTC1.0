import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox

from utils import error_catcher


class NewPasswordView(QWidget):
    b_pressed_submit_new_password = pyqtSignal(object, object, object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.otp_entry = None
        self.password_input = None
        self.confirm_password_input = None
        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        layout = QVBoxLayout()
        otp_label = QLabel('Enter the code sent to your email.')
        self.otp_entry = QLineEdit()
        self.otp_entry.setPlaceholderText('Enter OTP here.')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter new password.')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Confirm new password.')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        button_go_back = QPushButton('Cancel')
        button_submit_new_password = QPushButton('Continue')

        layout.addWidget(button_go_back)
        layout.addWidget(otp_label)
        layout.addWidget(self.otp_entry)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addStretch()
        layout.addWidget(button_submit_new_password)
        self.setLayout(layout)

        otp_label.setObjectName('NPV_otp_label')
        button_go_back.setObjectName('NPV_button_go_back')
        button_submit_new_password.setObjectName('NPV_button_submit_new_password')

        self.otp_entry.returnPressed.connect(button_submit_new_password.click)
        self.password_input.returnPressed.connect(button_submit_new_password.click)
        self.confirm_password_input.returnPressed.connect(button_submit_new_password.click)

        button_go_back.clicked.connect(self.button_pressed_go_back)
        button_submit_new_password.clicked.connect(self.button_pressed_submit_password)

    def button_pressed_go_back(self):
        self.b_pressed_go_back.emit()

    def button_pressed_submit_password(self):
        try:
            otp_entered = self.otp_entry.text()
            password = self.password_input.text()
            confirm_password = self.confirm_password_input.text()
            self.b_pressed_submit_new_password.emit(otp_entered, password, confirm_password)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, 'Error', 'An error occurred. Please try again.')
