import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, \
    QStackedWidget, QLabel

from main_window.MainWindowViewModel import MainWindowViewModel
from utils import ResizableWindow
from main_window.bottom_frame.friend_list.FriendsListView import FriendsListView
from main_window.bottom_frame.personal_account_view.PersonalAccountView import PersonalAccountsView


class MainWindowTopBar(QFrame):
    b_pressed_friend_list_view = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_bar_layout = None
        self.switch_view_button = None
        self.button_friend_list_view = None

        self.window_functions_layout = None
        self.close_app_button = None
        self.expand_shrink_button = None
        self.minimize_button = None

        self.setObjectName('mm_top_frame')
        self.initializeGUI()
        
        self.button_friend_list_view.clicked.connect(lambda: self.b_pressed_friend_list_view.emit())

    def initializeGUI(self):
        try:
            self.top_bar_layout = QHBoxLayout(self)
            self.initializeFrameButtons()
            self.setLayout(self.top_bar_layout)
        except Exception as e:
            print(f'Error setting up top frame: {e}')

    def create_button(self, icon_name, callback=None):
        """
        Helper method to create a button with an icon.
        """
        try:
            button = QPushButton("")
            button.setIcon(self.parent().icons[f'{icon_name}'])
            button.setObjectName(icon_name)
            if callback:
                button.clicked.connect(callback)
            return button
        except Exception as e:
            print(f'Error creating button: {e}')

    def initializeFrameButtons(self):
        try:
            """ FRIENDS LIST BUTTON & SWITCH VIEW BUTTON """
            self.button_friend_list_view = self.create_button("friends_icon")
            self.switch_view_button = self.create_button("switch_views")

            """ WINDOW FUNCTIONS BUTTONS """
            self.minimize_button = self.create_button("minimize_icon", self.parent().showMinimized)
            self.expand_shrink_button = self.create_button("expand_icon")
            self.close_app_button = self.create_button("close_icon", sys.exit)

            """ SEPARATE LAYOUT FOR WINDOW FUNCTIONS BUTTONS """
            self.window_functions_layout = QHBoxLayout()
            self.window_functions_layout.addWidget(self.minimize_button)
            self.window_functions_layout.addWidget(self.expand_shrink_button)
            self.window_functions_layout.addWidget(self.close_app_button)

            self.top_bar_layout.addWidget(self.button_friend_list_view)
            self.top_bar_layout.addWidget(self.switch_view_button)
            self.top_bar_layout.addSpacerItem(QSpacerItem(int(self.geometry().width() * 5),
                                                          int(self.geometry().height()),
                                                          QSizePolicy.Fixed,
                                                          QSizePolicy.Minimum))
            self.top_bar_layout.addLayout(self.window_functions_layout)
        except Exception as e:
            print(f'Error setting up top frame buttons: {e}')


class BottomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_stack = None
        self.bottom_frame_layout = None
        self.tradeFeedView = None
        self.personalAccountView = None
        self.friends_list_side_menu = None

        self._is_trade_feed_view = False

        self.setObjectName('mm_bottom_frame')
        self.initializeGUI()
        self.setLayout(self.bottom_frame_layout)

    def initializeGUI(self):
        try:
            self.bottom_frame_layout = QHBoxLayout(self)
            self.main_stack = QStackedWidget(self)

            self.registerInitialWidgets()
        except Exception as e:
            print(f'Error setting up bottom frame: {e}')

    """ REGISTERING BOTTOM FRAME WIDGETS. """

    def registerInitialWidgets(self):
        self.initializeFriendsMenu()
        self.initializePersonalAccountView()
        self.initializeTradeFeedView()
        self.main_stack.addWidget(self.personalAccountView)
        self.main_stack.setCurrentWidget(self.personalAccountView)
        self.main_stack.addWidget(self.tradeFeedView)

        self.bottom_frame_layout.addWidget(self.friends_list_side_menu, alignment=Qt.AlignTop)
        self.bottom_frame_layout.addWidget(self.main_stack)

    """ BOTTOM FRAME WIDGETS """

    def initializeFriendsMenu(self):
        try:
            self.friends_list_side_menu = FriendsListView()
            self.friends_list_side_menu.setMaximumWidth(0)
        except Exception as e:
            print(f'Error setting up friends side menu: {e}')

    def initializePersonalAccountView(self):
        try:
            self.personalAccountView = PersonalAccountsView(self)
            self.personalAccountView.setObjectName('personal_account_view')
        except Exception as e:
            print(f'Error initializing personal account view: {e}')

    def initializeTradeFeedView(self):
        try:
            self.tradeFeedView = QLabel('Trade Feed View')
            self.tradeFeedView.setObjectName('trade_feed_view')
        except Exception as e:
            print(f'Error initializing trade feed view: {e}')

    def switch_views(self):
        if self._is_trade_feed_view is False:
            self._is_trade_feed_view = True
            self.main_stack.setCurrentWidget(self.tradeFeedView)
        else:
            self._is_trade_feed_view = False
            self.main_stack.setCurrentWidget(self.personalAccountView)


class MainWindowView(ResizableWindow):
    def __init__(self):
        super().__init__()
        self.view_model, self.icons = self.init_view_model()
        self.top_bar = None
        self.bottom_frame = None

        self.setWindowTitle('JournalTrade')
        self.setObjectName('MainWindow')
        self.setMouseTracking(True)

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(int(screen.width() * 0.7), int(screen.height() * 0.7), int(screen.width() * 0.7),
                         int(screen.height() * 0.7))

        self.initializeGUI()
        self.init_bindings()

    def initializeGUI(self):
        self.top_bar = MainWindowTopBar(self)
        self.bottom_frame = BottomFrame(self)

        self.layout.addWidget(self.top_bar)
        self.layout.addWidget(self.bottom_frame)
        self.view_model.center_window(self)

    def init_view_model(self):
        self.view_model = MainWindowViewModel()
        self.view_model.load_style_sheet(self)
        self.icons = self.view_model.load_icons()
        return self.view_model, self.icons

    def init_bindings(self):
        self.top_bar.expand_shrink_button.clicked.connect(lambda:
                                                          self.view_model.expand_shrink_button_pressed(self,
                                                                                                       self.top_bar))
        self.top_bar.button_friend_list_view.clicked.connect(lambda:
                                                         self.view_model.friends_list_button_pressed(self.top_bar,
                                                                                                     self.bottom_frame))

        self.top_bar.switch_view_button.clicked.connect(self.bottom_frame.switch_views)



def main():
    app = QApplication(sys.argv)
    window = MainWindowView()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
