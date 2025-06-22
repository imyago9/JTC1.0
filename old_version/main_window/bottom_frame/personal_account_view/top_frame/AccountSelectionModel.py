import logging

from PyQt5.QtCore import QObject

from old_version.utils import error_catcher

from old_version.main_window.UserSessionModel import UserSessionModel


class AccountSelectionModel(QObject):
    def __init__(self):
        super().__init__()
        self.user_session = UserSessionModel()
        self.user_id = self.user_session.get_user_id()

    @error_catcher(log_func=logging.error, default_return=None)
    def get_all_accounts(self, user_id, account_type=None):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                if account_type:
                    cursor.execute(self.user_session.get_query('select_accounts_from_type_query'), (user_id, account_type))
                else:
                    cursor.execute(self.user_session.get_query('select_all_accounts_query'), (user_id,))
                conn.commit()
                accounts = cursor.fetchall()
                return accounts
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def insert_account(self, user_id, account_name, account_type):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('insert_new_account_query'), (user_id, account_name, account_type))
                conn.commit()
                return True
        finally:
            if conn:
                self.user_session.release_connection(conn)
