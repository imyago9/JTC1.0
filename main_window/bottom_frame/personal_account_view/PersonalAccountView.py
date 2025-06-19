from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

from main_window.bottom_frame.personal_account_view.top_frame.AccountSelectionView import AccountSelectionView
from main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.AccountInformationView import AccountInformationView

from main_window.bottom_frame.personal_account_view.PersonalAccountViewModel import PersonalAccountViewModel


class PersonalAccountsView(QWidget):
    disable_account_list_signal = pyqtSignal()
    PAV_updates_AIV = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model, self.icons = self.initialize_view_model()

        self.main_layout = None
        self.top_frame_layout = None
        self.button_select_account = None
        self.account_selection_view = None

        self.account_information_view = None

        self._is_account_selection_view = False

        self.initializeGUI()
        self.set_object_names()

    def initializeGUI(self):
        self.main_layout = QVBoxLayout()
        self.init_top_frame()
        self.init_bottom_frame()
        self.setLayout(self.main_layout)

    def init_top_frame(self):
        try:
            self.top_frame_layout = QHBoxLayout()
            self.button_select_account = QPushButton("Select a Account.")

            self.account_selection_view = AccountSelectionView(self)

            self.top_frame_layout.addWidget(self.button_select_account, alignment=Qt.AlignCenter)
            self.top_frame_layout.addWidget(self.account_selection_view, alignment=Qt.AlignCenter)
            self.main_layout.addLayout(self.top_frame_layout)

            self.account_selection_view.hide()
            self.button_select_account.clicked.connect(self.toggle_account_selection_view)

            self.account_selection_view.b_pressed_account_name_selected.connect(self.view_model.setupAccountSelection)
        except Exception as e:
            print(f'Error setting up top frame: {e}')

    def toggle_account_selection_view(self):
        try:
            if self._is_account_selection_view:
                self.button_select_account.setText("Select a Account.")
                self.account_selection_view.hide()
                self._is_account_selection_view = False
                print('hiding account selection view')
            else:
                self.button_select_account.setText("Close")
                self.account_selection_view.show()
                self._is_account_selection_view = True
                print('showing account selection view')

        except Exception as e:
            print(f"Failed to toggle popup: {e}")

    def init_bottom_frame(self):
        try:

            self.account_information_view = AccountInformationView(self)
            self.view_model.account_selected.connect(self.handle_account_selected)

            layout = QVBoxLayout()
            layout.addWidget(self.account_information_view)
            self.main_layout.addLayout(layout)
        except Exception as e:
            print(f'Error setting up bottom frame: {e}')

    def handle_account_selected(self):
        self.toggle_account_selection_view()  # Toggles of displaying 'Select an Account' button again.
        self.PAV_updates_AIV.emit()

    def setupVisibility(self, money_visible):
        """Updates the money visibility icon based on the account's visibility setting."""
        try:
            icon = self.icons['hide'] if money_visible else self.icons['view']
            # self.account_information_view.stats_frame.money_visibility_button.setIcon(icon)
        except Exception as e:
            print(f'Error setting up visibility: {e}')

    def set_object_names(self):
        self.button_select_account.setObjectName('pv_top_frame_title')
        # self.account_information_view.setObjectName('pv_graphs_frame')

    def initialize_view_model(self):
        self.view_model = PersonalAccountViewModel(self)
        self.view_model.load_style_sheet(self)
        self.icons = self.view_model.load_icons()
        return self.view_model, self.icons

