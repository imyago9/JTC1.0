from PyQt5.QtCore import QObject

from db_connection import db_connection


class UserSessionModel(QObject):
    _instance = None
    user_id = None
    personal_account_session = None
    db = db_connection()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSessionModel, cls).__new__(cls)
            cls._instance.user_id = None
        return cls._instance

    def get_connection(self):
        return self.db.get_connection()

    def release_connection(self, conn):
        return self.db.release_connection(conn)

    def get_query(self, query):
        return self.db.get_query(query)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def start_personal_account_session(self):
        if self.personal_account_session is None:
            self.personal_account_session = PersonalAccountSession()
        return self.personal_account_session


class PersonalAccountSession(QObject):
    _instance = None
    account_id = None
    trade_data = None
    stats_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonalAccountSession, cls).__new__(cls)
            cls._instance.account_id = None
            cls._instance.trade_data = None
            cls._instance.stats_data = None
        return cls._instance

    def set_stats_data(self, stats_data):
        self.stats_data = stats_data

    def get_stats_data(self):
        return self.stats_data

    def set_trade_data(self, trade_data):
        self.trade_data = trade_data

    def get_trade_data(self):
        return self.trade_data

    def set_current_account(self, account_id):
        self.account_id = account_id
        print('Current account id set to:', account_id)

    def get_current_account(self):
        return self.account_id

