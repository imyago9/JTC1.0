from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QLabel, QPushButton, QStackedWidget, QScrollArea,
                             QHBoxLayout, QLineEdit)

from main_window.bottom_frame.friend_list.FriendsListViewModel import FriendsListViewModel


class FriendsListView(QWidget):
    def __init__(self):
        super().__init__()
        self.view_model = self.init_view_model()

        self.animation = self.setupAnimation()
        self.main_layout = None
        self.initializeGUI()
        self.init_bindings()
        self.view_model.update_friends_list(self.friend_list_frame)

    def setupAnimation(self):
        try:
            animation = QPropertyAnimation(self, b"maximumWidth")
            animation.setDuration(600)
            return animation
        except Exception as e:
            print(f'Failed to setup animation: {e}')

    def startAnimation(self, target_width):
        try:
            current_width = self.maximumWidth()
            self.animation.stop()
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(target_width if current_width == 0 else 0)
            self.animation.start()
        except Exception as e:
            print(f'Failed to start animation: {e}')

    def initializeGUI(self):
        try:
            self.main_layout = QVBoxLayout(self)
            self.setupTopFrame()
            self.setupBottomFrame()
            self.main_layout.addStretch()
        except Exception as e:
            print(f'Failed to initialize GUI: {e}')

    def setupTopFrame(self):
        header_layout = QVBoxLayout()
        self.menu_title = QLabel('Friend\'s List')
        self.add_friend_button = QPushButton("Add Friend")
        self.requests_button = QPushButton("Requests")
        self.input_layout = QVBoxLayout()

        header_layout.addWidget(self.menu_title, alignment=Qt.AlignCenter)
        header_layout.addWidget(self.add_friend_button)
        header_layout.addWidget(self.requests_button)

        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(self.input_layout)

        self.menu_title.setObjectName('FLV_menu_title')
        self.add_friend_button.setObjectName('FLV_add_friend_button')
        self.requests_button.setObjectName('FLV_requests_button')

    def setupBottomFrame(self):
        self.stack = QStackedWidget()

        self.friend_list_frame = self.createScrollableFrame()
        self.friend_request_list_frame = self.createScrollableFrame()

        self.stack.addWidget(self.friend_list_frame)
        self.stack.addWidget(self.friend_request_list_frame)
        self.stack.setCurrentWidget(self.friend_list_frame)

        self.main_layout.addWidget(self.stack)

    @staticmethod
    def createScrollableFrame():
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(0)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameStyle(QFrame.NoFrame)
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)
        scroll_content.setLayout(scroll_content_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        return frame

    @staticmethod
    def display_blank_friend_list_view(frame, message):
        scroll_content_layout = frame.findChild(QVBoxLayout)
        # Clear existing content
        for i in reversed(range(scroll_content_layout.count())):
            widget = scroll_content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add placeholder message
        placeholder_label = QLabel(message)
        placeholder_label.setAlignment(Qt.AlignCenter)
        scroll_content_layout.addWidget(placeholder_label)

        placeholder_label.setObjectName('FLV_placeholder_label')

    def update_lists(self, frame, data, is_request=False):
        scroll_content_layout = frame.findChild(QVBoxLayout)
        for i in reversed(range(scroll_content_layout.count())):
            widget = scroll_content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for item in data:
            if is_request:
                self.setup_friend_request_list_items(scroll_content_layout, *item)
            else:
                self.setup_friend_list_items(scroll_content_layout, item)

    @staticmethod
    def setup_friend_list_items(layout, item):
        friend_name = QLabel(item[0])
        layout.addWidget(friend_name)

        friend_name.setObjectName('FLV_friend_name')

    def setup_friend_request_list_items(self, layout, friend_name, friend_id):
        friend_label = QLabel(f'✦ {friend_name}')
        accept_button = self.create_friend_request_response_button(
            "Accept", lambda: self.view_model.accept_friend_request_pressed(
                                                    friend_id, self.friend_request_list_frame))

        reject_button = self.create_friend_request_response_button(
            "Reject", lambda: self.view_model.reject_friend_request_pressed(
                                                    friend_id, self.friend_request_list_frame))

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(accept_button)
        buttons_layout.addWidget(reject_button)
        item_layout = QVBoxLayout()
        item_layout.addWidget(friend_label)
        item_layout.addLayout(buttons_layout)
        item_frame = QFrame()
        item_frame.setLayout(item_layout)
        layout.addWidget(item_frame)

        friend_label.setObjectName('FLV_friend_name')
        item_frame.setObjectName('FLV_friend_request_item')
        accept_button.setObjectName('FLV_accept_button')
        reject_button.setObjectName('FLV_reject_button')

    @staticmethod
    def create_friend_request_response_button(text, callback):
        button = QPushButton(text)
        button.setObjectName(f'{text.lower()}_request_button')
        button.clicked.connect(callback)
        return button

    @staticmethod
    def changeButtonAction(button, text, action=None):
        button.setText(text)
        button.disconnect()
        button.clicked.connect(action)

    def switchToFriendRequestView(self):
        try:
            self.menu_title.setText('Friend Requests')
            self.changeButtonAction(self.add_friend_button, 'Go Back', self.switchToFriendsListView)
            self.changeButtonAction(self.requests_button, '-', print)
            self.stack.setCurrentWidget(self.friend_request_list_frame)
            self.view_model.update_friend_request_list(self.friend_request_list_frame)
        except Exception as e:
            print(f'Failed to check friend requests: {e}')

    def switchToAddFriendView(self):
        self.menu_title.setText('Add a Friend')
        self.requests_button.setVisible(False)
        self.friend_input = QLineEdit()
        self.friend_input.setObjectName('FLV_friend_input')
        self.friend_input.setPlaceholderText("Enter friend's name")
        self.submit_button = QPushButton('Send Request')
        self.submit_button.setObjectName('FLV_button_submit_request')
        self.submit_button.clicked.connect(lambda:
                                           self.view_model.submit_friend_request_pressed(self.friend_input.text()))
        self.changeButtonAction(self.add_friend_button, 'Go Back', self.switchToFriendsListView)
        self.input_layout.addWidget(self.friend_input)
        self.input_layout.addWidget(self.submit_button)

    def switchToFriendsListView(self):
        try:
            self.menu_title.setText("Friend's List")
            if not self.requests_button.isVisible():
                self.requests_button.setVisible(True)
            if self.requests_button.text() == '-':
                self.changeButtonAction(self.requests_button, 'Requests',
                                        self.view_model.activate_friend_request_view_pressed)
            self.changeButtonAction(self.add_friend_button, 'Add Friend',
                                    self.view_model.activate_add_friend_view_pressed)
            widgets = [self.friend_input if hasattr(self, 'friend_input') else None,
                       self.submit_button if hasattr(self, 'submit_button') else None]
            if widgets:
                for widget in widgets:
                    if widget:
                        widget.setParent(None)
            self.stack.setCurrentWidget(self.friend_list_frame)
            self.view_model.update_friends_list(self.friend_list_frame)
        except Exception as e:
            print(f'Failed to go back from add friend: {e}')

    def init_bindings(self):
        self.view_model.b_pressed_display_friend_list.connect(self.startAnimation)
        self.view_model.show_empty_list.connect(self.display_blank_friend_list_view)
        self.view_model.update_list.connect(self.update_lists)

        self.view_model.addFriendViewPressedSignal.connect(self.switchToAddFriendView)
        self.view_model.friendRequestViewPressedSignal.connect(self.switchToFriendRequestView)
        self.view_model.friendListViewPressedSignal.connect(self.switchToFriendsListView)

        self.add_friend_button.clicked.connect(self.view_model.activate_add_friend_view_pressed)
        self.requests_button.clicked.connect(self.view_model.activate_friend_request_view_pressed)

    def init_view_model(self):
        self.view_model = FriendsListViewModel(self)
        self.view_model.load_style_sheet(self)
        return self.view_model
