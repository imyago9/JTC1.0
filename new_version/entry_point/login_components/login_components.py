from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QWidget, QMessageBox, QLabel


class LoginView(QWidget):
    b_pressed_register = pyqtSignal()
    b_pressed_forgot_pass = pyqtSignal()
    b_pressed_login = pyqtSignal(object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_input = None
        self.username_input = None

        self.init_gui()

    def init_gui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        button_forgot_password = QPushButton('Forgot Password')
        self.button_login = QPushButton('Login')
        self.button_register = QPushButton('Register')
        layout.addStretch()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button_forgot_password)
        layout.addStretch()
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)
        self.setLayout(layout)

        button_forgot_password.setObjectName('LV_button_forgot_password')
        self.username_input.setObjectName('LV_username_input')
        self.password_input.setObjectName('LV_password_input')
        self.button_login.setObjectName('LV_button_login')
        self.button_register.setObjectName('LV_button_register')

        # self.username_input.returnPressed.connect(self.button_login.click)
        # self.password_input.returnPressed.connect(self.button_login.click)

        button_forgot_password.clicked.connect(self.button_pressed_forgot_password)
        self.button_login.clicked.connect(self.button_pressed_login)
        self.button_register.clicked.connect(self.button_pressed_register)

    def lv_reset_text(self):
        self.username_input.setPlaceholderText('Username')
        self.username_input.clear()
        self.username_input.setFocus()

        self.password_input.setPlaceholderText('Password')
        self.password_input.clear()

    def button_pressed_forgot_password(self):
        self.b_pressed_forgot_pass.emit()

    def button_pressed_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.b_pressed_login.emit(username, password)

    def button_pressed_register(self):
        self.b_pressed_register.emit()


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

class ForgotPassView(QWidget):
    b_pressed_submit_email = pyqtSignal(object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.email_input = None
        self.init_gui()

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

class TwoFactorAuthView(QWidget):
    b_pressed_submit_otp = pyqtSignal(object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.otp_entry = None
        self.init_gui()

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

class NewPasswordView(QWidget):
    b_pressed_submit_new_password = pyqtSignal(object, object, object)
    b_pressed_go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.otp_entry = None
        self.password_input = None
        self.confirm_password_input = None
        self.init_gui()

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
