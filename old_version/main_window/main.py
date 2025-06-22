# This file is the entry point for the application. It initializes the main window and sets up logging.

from old_version.main_window.MainWindowView import MainWindowView
from old_version.utils import load_stylesheet
import logging
from old_version.main_window.UserSessionModel import UserSessionModel


def execute_app(user_id):
    try:
        user_session = UserSessionModel()
        user_session.set_user_id(user_id)
        window = MainWindowView()
        load_stylesheet(window, 'main_window_style')
        window.show()
        print('Journal-Trade main window opened.')
    except Exception as e:
        logging.error(f'Error initializing main window: {e}')
