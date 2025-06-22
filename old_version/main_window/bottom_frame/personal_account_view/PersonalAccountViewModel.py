from PyQt5.QtCore import QObject, pyqtSignal

from old_version.utils import ResourceLoader as RL, load_stylesheet

from old_version.main_window.bottom_frame.personal_account_view.PersonalAccountModel import PersonalAccountModel


class PersonalAccountViewModel(QObject):
    account_selected = pyqtSignal()
    trade_data = pyqtSignal(dict)
    trade_stats = pyqtSignal(dict)
    refreshMoneyVisibility = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = PersonalAccountModel()
        self.user_session = self.model.user_session
        self.personal_account_session = self.model.personal_account_session
        self.icons = {}

        self.current_account = None

    def load_icons(self):
        self.icons = {
            "view": RL.get_icon("pv_view"),
            "hide": RL.get_icon("pv_hide"),
            "add_trade": RL.get_icon("pv_add_trade"),
            "cancel_trade": RL.get_icon("pv_cancel_trade_update")
        }
        return self.icons

    @staticmethod
    def load_style_sheet(self):
        load_stylesheet(self, 'personal_acc_view')

    def setupAccountSelection(self, account_id, account_name):
        try:
            new_title = f"{account_name}"
            if self.current_account != new_title:
                self.current_account = new_title
                self.personal_account_session.set_current_account(account_id)
                self.account_selected.emit()
            else:
                # Improve handling for accounts that already are selected.
                print(f"Account {account_name} is already selected.")
        except Exception as e:
            print(f'Failed to update account data: {e}')



