from PyQt5.QtCore import QObject

from old_version.utils import ResourceLoader as RL, center_window, load_stylesheet


class MainWindowViewModel(QObject):
    def __init__(self):
        super().__init__()
        self.icons = {}

        self.current_selected_account = None

        self.isTradeFeedView = False

        self.isFriendsListView = False

    def load_icons(self):
        self.icons = {
            'friends_icon': RL.get_icon('friends_icon'),
            'switch_views': RL.get_icon('switch_views'),
            'minimize_icon': RL.get_icon('minimize_icon'),
            'expand_icon': RL.get_icon('expand_icon'),
            'close_icon': RL.get_icon('close_icon')}
        return self.icons

    @staticmethod
    def load_style_sheet(parent):
        try:
            return load_stylesheet(parent, 'main_window_style')
        except Exception as e:
            print(f'Error loading style sheet: {e}')

    @staticmethod
    def center_window(parent):
        try:
            return center_window(parent)
        except Exception as e:
            print(f'Error centering window: {e}')

    def friends_list_button_pressed(self, top_bar, bottom_frame):
        try:
            """
            Toggle the friends list side menu visibility with encapsulated animation logic.
            """
            self.isFriendsListView = bottom_frame.friends_list_side_menu.view_model.activate_view_button_pressed(
                self.isFriendsListView,
                int(top_bar.friends_view_button.width()))
        except Exception as e:
            print(f'Error toggling friends menu: {e}')

    @staticmethod
    def expand_shrink_button_pressed(parent, top_bar):
        try:
            if parent.isFullScreen():
                parent.showNormal()
                top_bar.expand_shrink_button.setIcon(top_bar.icons['expand_icon'])
            else:
                parent.showFullScreen()
                top_bar.expand_shrink_button.setIcon(top_bar.icons['minimize_icon'])
        except Exception as e:
            print(f"Error toggling window size: {e}")

