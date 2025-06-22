from PyQt5.QtCore import QObject, pyqtSignal

from old_version.main_window.bottom_frame.personal_account_view.top_frame.AccountSelectionModel import AccountSelectionModel
from old_version.utils import load_stylesheet, show_message


class AccountSelectionViewModel(QObject):
    account_changed = pyqtSignal([int, str])
    b_pressed_add_account = pyqtSignal([str])
    b_pressed_create_account = pyqtSignal([str])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = AccountSelectionModel()
        self.user_id = self.model.user_id

        self.selected_account_type = None

    @staticmethod
    def load_style_sheet(self):
        load_stylesheet(self, 'accounts_styles')

    def get_all_accounts(self, account_type=None):
        return self.model.get_all_accounts(self.user_id, account_type)

    def insert_account(self, account_name, account_type):
        return self.model.insert_account(self.user_id, account_name, account_type)

    def accountSelected(self, acc_id, acc):
        """
        Handle account selection.
        """
        try:
            self.account_changed.emit(acc_id, acc)
        except Exception as e:
            print(f'Failed to select account: {e}')

    def addAccountPressed(self):
        """
        Load the 'Create Account' view.
        """
        try:
            self.b_pressed_add_account.emit(self.selected_account_type)
        except Exception as e:
            print(f'Add account button did not work: {e}')

    def createAccount(self, account_name):
        """
        Create a new account and refresh the list.
        """
        try:
            if not account_name:
                show_message(self.parent(), "Invalid Input", "Account name cannot be empty.")
                return
            self.insert_account(account_name, self.selected_account_type)
            self.b_pressed_create_account.emit(self.selected_account_type)
            print(f'User {self.user_id} has created a new account called *{account_name}*, '
                  f'with the *{self.selected_account_type}* type')

        except Exception as e:
            print(f'Create account pressed failed: {e}')

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
