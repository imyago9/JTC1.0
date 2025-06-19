from enum import Enum

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QStackedWidget

from main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.AccountInformationViewModel import \
    AccountInformationViewModel
from main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.new_trade_view.NewTradeView import \
    NewTradeView
from main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.ThreeGraphView import \
    ThreeGraphView
from utils import ErrorPopup, show_message


class ViewStates(Enum):
    THREE_GRAPH_VIEW = 'three_graph_view'
    NEW_TRADE_VIEW = 'new_trade_view'
    TRADE_INFO_VIEW = 'trade_info_view'


class AccountInformationView(QFrame):
    AIV_updates_TGV = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = self.init_view_model()
        self.view_state = None

        self.main_stack = None
        self.views = None

        self.init_gui()
        self.set_object_names()
        self.init_bindings()
        print('AccountInformationView initialized')
        self.setFixedHeight(self.sizeHint().height())

    def init_gui(self):
        layout = QVBoxLayout(self)
        self.main_stack = QStackedWidget(self)

        self.views = {'three_graph': ThreeGraphView(self),
                      'new_trade': NewTradeView(self),
                      'trade_info': QFrame(self)}

        for widget in self.views.values():
            self.main_stack.addWidget(widget)

        layout.addWidget(self.main_stack)

        self.setLayout(layout)

    def displayThreeGraphView(self):
        try:
            if self.view_state == ViewStates.THREE_GRAPH_VIEW:
                return
            self.main_stack.setCurrentWidget(self.views['three_graph'])
            self.view_state = ViewStates.THREE_GRAPH_VIEW
        except Exception as e:
            print(f'Failed to toggle three graph view: {e}')

    def displayNewTradeView(self):
        try:
            if self.view_state == ViewStates.NEW_TRADE_VIEW:
                return
            self.views['new_trade'].set_return_button_visible(False)
            self.main_stack.setCurrentWidget(self.views['new_trade'])
            self.view_state = ViewStates.NEW_TRADE_VIEW
        except Exception as e:
            print(f'Failed to toggle new trade view: {e}')

    def update_account(self):
        try:
            self.view_model.load_trades()
        except Exception as e:
            print(f'Error updating account information: {e}')

    def display_updated_account(self):
        try:
            self.AIV_updates_TGV.emit()
            self.displayThreeGraphView()
        except Exception as e:
            print(f'Error displaying updated account: {e}')

    def new_trade_button_pressed(self):
        try:
            if self.view_model.current_account():
                self.displayNewTradeView()
                self.views['new_trade'].set_return_button_visible(True)
            else:
                show_message(self.parent(), 'Error', 'No Account Selected')
        except Exception as e:
            print(f'Failed to toggle new trade button: {e}')

    def init_bindings(self):
        self.view_model.trade_data_updated.connect(self.display_updated_account)
        self.views['new_trade'].trade_created.connect(self.update_account)

        self.parent().PAV_updates_AIV.connect(self.update_account)

    def set_object_names(self):
        self.views['three_graph'].stats_label_view.setObjectName('pv_stats_frame')
        self.views['three_graph'].stats_label_view.first_stats_label.setObjectName('pv_first_stats_label')
        self.views['three_graph'].stats_label_view.second_stats_label.setObjectName('pv_second_stats_label')
        self.views['three_graph'].stats_label_view.third_stats_label.setObjectName('pv_third_stats_label')

        self.views['three_graph'].stats_label_view.money_visibility_button.setObjectName('pv_stats_buttons')
        self.views['three_graph'].stats_label_view.add_new_trade_button.setObjectName('pv_stats_buttons')

    def init_view_model(self):
        self.view_model = AccountInformationViewModel(self)
        self.view_model.load_style_sheet(self)
        return self.view_model
