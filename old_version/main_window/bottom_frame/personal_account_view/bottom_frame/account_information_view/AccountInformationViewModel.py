from PyQt5.QtCore import QObject, pyqtSignal

from old_version.main_window.bottom_frame.personal_account_view.PersonalAccountModel import PersonalAccountModel
from old_version.utils import load_stylesheet


class AccountInformationViewModel(QObject):
    trade_data_updated = pyqtSignal()
    empty_trade_data = pyqtSignal()
    full_trade_data = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = PersonalAccountModel()

    def current_account(self):
        return self.model.personal_account_session.get_current_account()

    @staticmethod
    def load_style_sheet(self):
        load_stylesheet(self, 'account_information_view')

    def get_trade_data(self):
        try:
            account_id = self.model.personal_account_session.get_current_account()
            return self.model.fetchAccountData(account_id)
        except Exception as e:
            print(f'Error fetching trade data: {e}')

    def load_trades(self):
        try:
            trade_data = self.get_trade_data()
            if trade_data:
                s_date, e_date = self.model.determineDateRange()
                filtered_data = self.model.filterDataByDateRange(s_date, e_date)

                grouped_data = self.model.groupTradeData(filtered_data)
                grouped_data = self.model.assignTradeResults(grouped_data)
                stats = self.model.calculateTradeStats(grouped_data)
                self.model.personal_account_session.set_stats_data(stats)
                self.model.personal_account_session.set_trade_data(trade_data)
                self.trade_data_updated.emit()
                return
            if trade_data is None:
                self.parent().displayNewTradeView()
                print('Empty emitted')
                return
        except Exception as e:
            print(f'Error loading trades: {e}')

