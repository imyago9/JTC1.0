from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from utils import error_catcher
import logging


class ForgotPassView(QWidget):
    b_pressed_submit_email = pyqtSignal(object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.email_input = None
        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        layout = QVBoxLayout()
        label = QLabel('Enter your email.')
        self.email_input = QLineEdit()
        button_submit_email = QPushButton('Enter email')
        button_go_back = QPushButton('Back To Login')

        layout.addWidget(label)
        layout.addWidget(self.email_input)
        layout.addStretch()
        layout.addWidget(button_submit_email)
        layout.addWidget(button_go_back)
        self.setLayout(layout)

        label.setObjectName('FPV_label')
        button_submit_email.setObjectName('FPV_button_submit_email')
        button_go_back.setObjectName('FPV_button_go_back')

        self.email_input.returnPressed.connect(button_submit_email.click)
        button_submit_email.clicked.connect(self.button_pressed_submit_email)
        button_go_back.clicked.connect(self.button_pressed_go_back)

    def fpv_reset_text(self):
        self.email_input.setPlaceholderText('Email')
        self.email_input.clear()

    def button_pressed_submit_email(self):
        email = self.email_input.text()
        self.b_pressed_submit_email.emit(email)

    def button_pressed_go_back(self):
        self.b_pressed_go_back.emit()
