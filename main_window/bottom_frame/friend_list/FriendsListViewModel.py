from PyQt5.QtCore import QObject, pyqtSignal

from main_window.bottom_frame.friend_list.FriendsListModel import FriendsListModel
from utils import load_stylesheet


class FriendsListViewModel(QObject):
    b_pressed_display_friend_list = pyqtSignal(int)

    show_empty_list = pyqtSignal(object, str)
    update_list = pyqtSignal(object, object, bool)

    addFriendViewPressedSignal = pyqtSignal()
    friendRequestViewPressedSignal = pyqtSignal()
    friendListViewPressedSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = FriendsListModel()
        self.user_id = self.model.user_id

    @staticmethod
    def load_style_sheet(parent):
        try:
            return load_stylesheet(parent, 'friends_list_styles')
        except Exception as e:
            print(f'Error loading style sheet: {e}')

    def activate_view_button_pressed(self, isFriendsListView, target_width):
        """
        Animate the visibility of the friends list side menu.
        """
        isFriendsListView = not isFriendsListView
        self.b_pressed_display_friend_list.emit(target_width if isFriendsListView else 0)
        return isFriendsListView

    def submit_friend_request_pressed(self, friend_name):
        try:
            if friend_name:
                friend_id = self.model.username_to_userid(friend_name)
                if friend_id:
                    self.model.send_friend_request(self.user_id, friend_id)
                    print(f"Friend request sent to {friend_name}")
                self.friendListViewPressedSignal.emit()
        except Exception as e:
            print(f'Failed to send friend request: {e}')

    def activate_add_friend_view_pressed(self):
        try:
            self.addFriendViewPressedSignal.emit()
        except Exception as e:
            print(f'Failed to add friend: {e}')

    def activate_friend_request_view_pressed(self):
        try:
            self.friendRequestViewPressedSignal.emit()
        except Exception as e:
            print(f'Failed to check friend requests: {e}')

    def update_friends_list(self, frame):
        friends = self.model.get_friends(self.user_id, status='accepted')
        if not friends:
            self.show_empty_list.emit(frame, "No friends yet. Add some!")
        else:
            self.update_list.emit(frame, friends, False)

    def update_friend_request_list(self, frame):
        friend_requests = self.model.get_received_friend_requests(self.user_id)
        if not friend_requests:
            self.show_empty_list.emit(frame, "No friend requests\nat the moment.")
        else:
            user_ids = [friend[0] for friend in friend_requests]
            friend = [friend[1] for friend in friend_requests]
            self.update_list.emit(frame, zip(friend, user_ids), True)

    def accept_friend_request_pressed(self, friend_id, frame):
        self.model.accept_friend_request(self.user_id, friend_id)
        self.update_friend_request_list(frame)

    def reject_friend_request_pressed(self, friend_id, frame):
        self.model.reject_friend_request(self.user_id, friend_id)
        self.update_friend_request_list(frame)
