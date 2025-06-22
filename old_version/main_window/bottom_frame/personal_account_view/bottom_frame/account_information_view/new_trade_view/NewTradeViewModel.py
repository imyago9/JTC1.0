from PyQt5.QtCore import QObject

from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.new_trade_view.NewTradeModel import NewTradeModel


class NewTradeViewModel(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = NewTradeModel()
        self.view = parent

    def check_save_all_trade_information(self, trade_data, screenshots):
        self.model.check_save_all_trade_information(trade_data, screenshots)



