from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
from old_version.utils import error_catcher
import logging


class TwoFactorAuthView(QWidget):
    b_pressed_submit_otp = pyqtSignal(object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.otp_entry = None
        self.init_gui()

    @error_catcher(log_func=logging.error)
    def init_gui(self):
        layout = QVBoxLayout()

        otp_label = QLabel('A code has been sent to your email.')
        self.otp_entry = QLineEdit()
        self.otp_entry.setPlaceholderText('Enter OTP here.')
        button_go_back = QPushButton('Cancel')
        button_submit_otp = QPushButton('Enter OTP')

        layout.addWidget(button_go_back)
        layout.addWidget(otp_label)
        layout.addWidget(self.otp_entry)
        layout.addStretch()
        layout.addWidget(button_submit_otp)
        self.setLayout(layout)

        otp_label.setObjectName('TFAV_otp_label')
        button_go_back.setObjectName('TFAV_button_go_back')
        button_submit_otp.setObjectName('TFAV_button_submit_otp')

        self.otp_entry.returnPressed.connect(button_submit_otp.click)

        button_go_back.clicked.connect(self.button_pressed_go_back)
        button_submit_otp.clicked.connect(self.button_pressed_submit_otp)

    def button_pressed_go_back(self):
        self.b_pressed_go_back.emit()

    def button_pressed_submit_otp(self):
        otp_entered = self.otp_entry.text()
        self.b_pressed_submit_otp.emit(otp_entered)
