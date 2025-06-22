import os
import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox

from old_version.login_executable.user_database.AuthService import AuthService
from old_version.utils import resource_path, load_stylesheet, show_message


class LoginViewModel(QObject):
    _icon_cache = {}  # Cache to store loaded icons
    logged_in_id = pyqtSignal(int)
    RV_otp_validated = pyqtSignal()
    NPV_otp_validated = pyqtSignal()
    handle_b_pressed_create_account = pyqtSignal()
    handle_b_pressed_submit_email = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = AuthService()
        self.user_id = None
        self.icons = {'close_icon', 'minimize_icon', 'jt_logo_full'}
        self.otp = None
        self.new_account_parameters = {'email': None, 'username': None, 'password': None}
        self.login_parameters = {'username': None, 'password': None}
        self.new_pass_email = None

    @staticmethod
    def init_style_sheet(app):
        load_stylesheet(app, 'login_style')

    @classmethod
    def get_icon(cls, name):
        """
        Retrieves an icon from the resources/icons folder, caching it for performance.
        """
        # Check if the icon is already in the cache
        if name in cls._icon_cache:
            return cls._icon_cache[name]

        # Construct the full path to the icon
        icon_dir = resource_path("resources/icons")
        icon_path = os.path.join(icon_dir, f"{name}.png")
        if os.path.exists(icon_path):
            try:
                icon = QtGui.QIcon(icon_path)
                cls._icon_cache[name] = icon  # Cache the loaded icon
                return icon
            except Exception as e:
                raise RuntimeError(f"Error loading icon '{name}': {e}")
        else:
            raise FileNotFoundError(f"Icon '{name}' not found in {icon_dir}")

    def create_user(self, email, username, password):
        user_id = self.model.register_user(email, username, password)
        if user_id:
            print('User created successfully.')

    def verify_login(self, username, password):
        verification_status, user_id = self.model.verify_credentials(username, password)
        print('Verification Status:', verification_status)
        if verification_status:
            self.user_id = user_id
            return True
        else:
            return False

    def verify_rv_otp(self, otp):
        try:
            if not otp.isdigit() or not len(otp) == 6:
                show_message(self.parent(), 'Error', 'OTP must be a 6-digit number.')
                return
            if int(otp) == int(self.model.otp):
                self.RV_otp_validated.emit()
                self.create_user(**self.new_account_parameters)
                show_message(self.parent(), 'Success', 'OTP is valid.')
            else:
                show_message(self.parent(), 'Error', 'OTP is invalid.')
        except Exception as e:
            show_message(self.parent(), 'Error', str(e))

    def verify_npv_otp(self, otp, password, confirm_password):
        if not otp.isdigit() or not len(otp) == 6:
            show_message(self.parent(), 'Error', 'OTP must be a 6-digit number.')
            return
        if not otp or not password or not confirm_password:
            show_message(self.parent(), 'Error', 'It is required to fill out all fields.')
            return
        if int(otp) == int(self.model.otp):
            if password == confirm_password:
                self.model.update_password(self.new_pass_email, password)
                self.NPV_otp_validated.emit()
                show_message(self.parent(), 'Success', 'Password updated successfully.')
            else:
                show_message(self.parent(), 'Error', 'Passwords do not match.')
        else:
            show_message(self.parent(), 'Error', 'OTP is invalid.')

    def handle_rv_button_pressed_create_account(self, email, username, password, confirm_password):
        if not email or not username or not password or not confirm_password:
            show_message(self.parent(), 'Error', 'It is required to fill out all fields.')
            return
        if password != confirm_password:
            show_message(self.parent(), 'Error', 'Passwords do not match.')
            return
        if self.model.check_if_identifier_exists(email):
            show_message(self.parent(), 'Error', 'Email already exists.')
            return
        if self.model.check_if_identifier_exists(username):
            show_message(self.parent(), 'Error', 'Username already exists.')
            return
        self.new_account_parameters = {
            'email': email,
            'username': username,
            'password': password}
        self.model.send_otp(email)
        self.handle_b_pressed_create_account.emit()

    def handle_lv_button_pressed_login(self, username, password):
        try:
            if not username or not password:
                show_message(self.parent(), 'Error', 'It is required to fill out all fields.')
                return
            if not self.model.check_if_identifier_exists(username):
                show_message(self.parent(), 'Error', 'No account with this username.')
                return
            verification_status = self.verify_login(username, password)
            if verification_status:
                self.open_main_window_view()
                self.parent().close()
            else:
                show_message(self.parent(), 'Login', 'Login failed')
        except Exception as e:
            show_message(self.parent(), "Error", str(e))

    def handle_fpv_button_pressed_submit_email(self, email):
        try:
            if self.model.check_if_identifier_exists(email):
                self.new_pass_email = email
                self.model.send_otp(email)
                self.handle_b_pressed_submit_email.emit()
            else:
                show_message(self.parent(), 'Error', 'No account with this email.')
        except Exception as e:
            QMessageBox.warning(self.parent(), "Error", str(e))

    def open_main_window_view(self):
        try:
            from old_version.main_window.main import execute_app
            execute_app(self.user_id)
        except Exception as e:
            logging.error(f"Error opening main window: {e}")

