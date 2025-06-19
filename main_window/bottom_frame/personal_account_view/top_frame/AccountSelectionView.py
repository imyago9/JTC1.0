from enum import Enum

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

from main_window.bottom_frame.personal_account_view.top_frame.AccountSelectionViewModel import AccountSelectionViewModel


class ViewSates(Enum):
    ACCOUNT_TYPE_LIST = 0
    ACCOUNT_LIST = 1
    CREATE_ACCOUNT = 2


class AccountSelectionView(QWidget):
    b_pressed_account_name_selected = pyqtSignal([int, str])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = self.init_view_model()
        self.view_state = None
        self.main_stack = None
        self.button_go_back = None
        self.button_add_account = None
        self.account_list_scroll_area = None
        self.account_list_scroll_area_widget = None
        self.account_list_scroll_area_layout = None
        self.button_create_account = None
        self.input_account_name = None
        self.create_account_frame = None
        self.create_account_layout = None

        self.init_gui()
        self.init_bindings()
        self.display_account_type_list()
        self.set_object_names()

        self.hide()

    def init_gui(self):
        layout = QHBoxLayout(self)

        self.main_stack = QStackedWidget(self)

        self.button_go_back = QPushButton('Back')
        self.button_add_account = QPushButton('Add Account')

        self.account_list_scroll_area = QScrollArea(self)
        self.account_list_scroll_area_widget = QWidget()
        self.account_list_scroll_area_layout = QHBoxLayout(self.account_list_scroll_area_widget)
        self.config_scroll_area()

        self.button_create_account = QPushButton('Confirm')
        self.input_account_name = QLineEdit()
        self.input_account_name.setPlaceholderText('Pick a Name..')

        self.create_account_frame = QFrame()
        self.create_account_layout = QHBoxLayout(self.create_account_frame)

        self.create_account_layout.addWidget(self.button_create_account)
        self.create_account_layout.addWidget(self.input_account_name)

        self.main_stack.addWidget(self.account_list_scroll_area)
        self.main_stack.addWidget(self.create_account_frame)

        layout.addStretch()
        layout.addWidget(self.button_add_account)
        layout.addWidget(self.main_stack)
        layout.addWidget(self.button_go_back)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def config_scroll_area(self):
        self.account_list_scroll_area.setWidgetResizable(True)
        self.account_list_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.account_list_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.account_list_scroll_area.setWidget(self.account_list_scroll_area_widget)

    def set_object_names(self):
        self.button_go_back.setObjectName('ASV_button_go_back')
        self.button_add_account.setObjectName('ASV_button_add_account')
        self.account_list_scroll_area.setObjectName('ASV_account_list_scroll_area')
        self.account_list_scroll_area_widget.setObjectName('ASV_account_list_scroll_area_widget')
        self.input_account_name.setObjectName('ASV_input_account_name')
        self.button_create_account.setObjectName('ASV_button_create_account')

    def display_account_type_list(self):
        """
        Load the account type buttons into the scroll area.
        """
        try:
            if self.view_state != ViewSates.ACCOUNT_TYPE_LIST:
                self.view_state = ViewSates.ACCOUNT_TYPE_LIST
                self.clear_layout(self.account_list_scroll_area_layout)
                account_types = {
                    "Backtest\nAccounts": "Backtest",
                    "Live\nAccounts": "Manual_acc",
                }
                for label, account_type in account_types.items():
                    button = QPushButton(label)
                    button.setObjectName(f"ASV_button_{account_type.lower()}")
                    button.clicked.connect(lambda _, at=account_type: self.display_account_list(at))
                    self.account_list_scroll_area_layout.addWidget(button)

                self.main_stack.setCurrentWidget(self.account_list_scroll_area)
                self.button_go_back.setVisible(False)
                self.button_add_account.setVisible(False)
                self.button_add_account.setText("Add Account")

                self.button_add_account.clicked.disconnect()
                self.button_add_account.clicked.connect(self.view_model.addAccountPressed)
        except Exception as e:
            print(f'Failed to setup account options: {e}')

    def display_account_list(self, account_type):
        """
        Load a list of accounts of a specific type.
        """
        try:
            if self.view_state != ViewSates.ACCOUNT_LIST:
                self.view_state = ViewSates.ACCOUNT_LIST
                self.clear_layout(self.account_list_scroll_area_layout)
                self.view_model.selected_account_type = account_type

                accounts = self.view_model.get_all_accounts(account_type=account_type)
                if accounts:
                    for account_id, account_name, account_type in accounts:
                        button = QPushButton(account_name)
                        button.setObjectName('ASV_button_account_choice')
                        button.clicked.connect(lambda _, acc_id=account_id, acc_name=account_name:
                                               self.button_pressed_account_name_selected(acc_id, acc_name))
                        self.account_list_scroll_area_layout.addWidget(button)
                else:
                    label = QLabel("No accounts available.")
                    label.setObjectName('ASV_label_no_accounts')
                    self.account_list_scroll_area_layout.addWidget(label)

                self.button_add_account.setVisible(True)
                self.button_go_back.setVisible(True)
                self.button_add_account.setText("Add Account")

                self.button_add_account.clicked.disconnect()
                self.button_add_account.clicked.connect(self.view_model.addAccountPressed)

                self.main_stack.setCurrentWidget(self.account_list_scroll_area)
        except Exception as e:
            print(f'Failed to update account list: {e}')

    def button_pressed_account_name_selected(self, acc_id, acc_name):
        self.display_account_type_list()  # Returns to account types before closing.
        self.b_pressed_account_name_selected.emit(acc_id, acc_name)

    def handle_add_account_pressed(self, account_type):
        if self.view_state != ViewSates.CREATE_ACCOUNT:
            self.view_state = ViewSates.CREATE_ACCOUNT
            self.input_account_name.clear()
            self.button_add_account.setText("Cancel")
            self.button_add_account.clicked.disconnect()
            self.button_add_account.clicked.connect(lambda: self.display_account_list(account_type))
            self.button_go_back.setVisible(False)
            self.main_stack.setCurrentWidget(self.create_account_frame)

    def init_view_model(self):
        self.view_model = AccountSelectionViewModel(self)
        return self.view_model

    def init_bindings(self):
        self.button_create_account.clicked.connect(lambda:
                                                   self.view_model.createAccount(self.input_account_name.text()))
        self.button_go_back.clicked.connect(self.display_account_type_list)
        self.button_add_account.clicked.connect(self.view_model.addAccountPressed)

        self.view_model.b_pressed_add_account.connect(self.handle_add_account_pressed)
        self.view_model.b_pressed_create_account.connect(self.display_account_list)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
