from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QWidget, QLabel


class LoginView(QWidget):
    pressed_login = pyqtSignal(str, str)
    pressed_register = pyqtSignal()
    pressed_forgot_pass = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        # ╭─ Creating Widgets ──────────────────────────────────────────╮
        self.username = QLineEdit(placeholderText='Username', objectName='LV_username') # type: ignore
        self.password = QLineEdit(placeholderText='Password', objectName='LV_password', echoMode=QLineEdit.Password) # type: ignore
        self.b_forgot = QPushButton("Forgot Password",objectName="LV_forgot", clicked=self.pressed_forgot_pass, cursor=Qt.PointingHandCursor) # type: ignore
        self.b_login = QPushButton("Login", objectName="LV_login", clicked=lambda: self.pressed_login.emit(self.username.text(), self.password.text()), cursor=Qt.PointingHandCursor) # type: ignore
        self.b_register = QPushButton("Register", objectName="LV_register", clicked=self.pressed_register, cursor=Qt.PointingHandCursor) # type: ignore
        # ╭─ Adding Widgets to Layout ──────────────╮
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.b_forgot)
        layout.addStretch(1)
        layout.addWidget(self.b_login)
        layout.addWidget(self.b_register)
        # ╭─ Return pressed clicks login ─────────────────────╮
        self.username.returnPressed.connect(self.b_login.click) # type: ignore
        self.password.returnPressed.connect(self.b_login.click) # type: ignore


class RegisterView(QWidget):
    pressed_create_account = pyqtSignal(object, object, object, object)
    pressed_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # ╭─ Creating Widgets ──────────────────────────────────────────╮
        self.email = QLineEdit(placeholderText='Email*', objectName='RV_email') # type: ignore
        self.username = QLineEdit(placeholderText='Username*', objectName='RV_username') # type: ignore
        self.password = QLineEdit(placeholderText='Password*', objectName='RV_password', echoMode=QLineEdit.Password)# type: ignore
        self.confirm_password = QLineEdit(placeholderText='Confirm Password*', objectName='RV_confirm_password', echoMode=QLineEdit.Password)# type: ignore
        b_create_account = QPushButton('Create Account', cursor=Qt.PointingHandCursor, objectName='RV_create_account', # type: ignore
                                       clicked=lambda: self.pressed_create_account.emit(self.email.text(), # type: ignore
                                                                                        self.username.text(),
                                                                                        self.password.text(),
                                                                                        self.confirm_password.text()))
        b_back = QPushButton('Back To Login', objectName='RV_back', clicked=self.pressed_back, cursor=Qt.PointingHandCursor) # type: ignore
        # ╭─ Adding Widgets ────────────────────╮
        layout = QVBoxLayout(self)
        layout.addWidget(self.email)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)
        layout.addStretch()
        layout.addWidget(b_create_account)
        layout.addWidget(b_back)

class ForgotPassView(QWidget):
    pressed_submit_email = pyqtSignal(object)
    pressed_back = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.email_input = None
        self._build_ui()

    def _build_ui(self):
        # ╭─ Creating Widgets ──────────────────────────────────────────╮
        label = QLabel('Enter your email.', objectName='FPV_label') # type: ignore
        self.email = QLineEdit(placeholderText='Email', objectName='FPV_email_input') # type: ignore
        b_submit_email = QPushButton('Enter email', objectName='FPV_submit_email', clicked=lambda: self.pressed_submit_email.emit(self.email.text()), cursor=Qt.PointingHandCursor) # type: ignore
        b_back = QPushButton('Back To Login', objectName='FPV_back', clicked=self.pressed_back, cursor=Qt.PointingHandCursor) # type: ignore
        # ╭─ Adding Widgets ────────────────────╮
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.email)
        layout.addStretch()
        layout.addWidget(b_submit_email)
        layout.addWidget(b_back)

class TwoFactorAuthView(QWidget):
    pressed_submit_otp = pyqtSignal(object)
    pressed_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # ╭─ Creating Widgets ──────────────────────────────────────────╮
        otp_label = QLabel('A code has been sent to your email.', objectName='TFAV_label') # type: ignore
        self.otp = QLineEdit(placeholderText='Enter OTP here.', objectName='TFAV_otp') # type: ignore
        b_submit_otp = QPushButton('Enter OTP', objectName='TFAV_submit_otp', clicked=lambda: self.pressed_submit_otp.emit(self.otp.text()), cursor=Qt.PointingHandCursor) # type: ignore
        b_back = QPushButton('Cancel', objectName='TFAV_back', clicked=self.pressed_back, cursor=Qt.PointingHandCursor) # type: ignore
        # ╭─ Adding Widgets to Layout ──────────────╮
        layout = QVBoxLayout(self)
        layout.addWidget(otp_label)
        layout.addWidget(self.otp)
        layout.addStretch()
        layout.addWidget(b_submit_otp)
        layout.addWidget(b_back)
        # ╭─ Return pressed clicks submit OTP ─────────────────────╮
        self.otp.returnPressed.connect(b_submit_otp.click)

class NewPasswordView(QWidget):
    pressed_submit_password = pyqtSignal(object, object, object)
    pressed_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        # ╭─ Creating Widgets ──────────────────────────────────────────╮
        otp_label = QLabel('Enter the code sent to your email.', objectName='NPV_otp_label') # type: ignore
        self.otp = QLineEdit(placeholderText='Enter OTP here.', objectName='NPV_otp_entry') # type: ignore
        self.password = QLineEdit(placeholderText='Enter new password.', objectName='NPV_password_input', echoMode=QLineEdit.Password) # type: ignore
        self.confirm_password = QLineEdit(placeholderText='Confirm new password.', objectName='NPV_confirm_password_input', echoMode=QLineEdit.Password) # type: ignore
        b_back = QPushButton('Cancel', objectName='NPV_go_back', clicked=self.pressed_back, cursor=Qt.PointingHandCursor) # type: ignore
        b_submit_password = QPushButton('Continue', objectName='NPV_submit_new_password', clicked=lambda: self.pressed_submit_password.emit(self.otp.text(), self.password.text(), self.confirm_password.text()), cursor=Qt.PointingHandCursor) # type: ignore
        # ╭─ Adding Widgets to Layout ──────────────╮
        layout = QVBoxLayout(self)
        layout.addWidget(otp_label)
        layout.addWidget(self.otp)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)
        layout.addStretch()
        layout.addWidget(b_submit_password)
        layout.addWidget(b_back)
