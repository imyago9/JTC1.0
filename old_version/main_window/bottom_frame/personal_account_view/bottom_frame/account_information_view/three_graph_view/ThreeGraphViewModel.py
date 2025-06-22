from PyQt5.QtCore import QObject

from old_version.main_window.bottom_frame.personal_account_view.PersonalAccountModel import PersonalAccountModel


class ThreeGraphViewModel(QObject):
    def __init__(self):
        super().__init__()
        self.model = PersonalAccountModel()

    def get_stats_data(self):
        return self.model.personal_account_session.get_stats_data()

    def get_trade_data(self):
        return self.model.personal_account_session.get_trade_data()

