import logging
from PyQt5.QtCore import QObject

from old_version.utils import error_catcher

from old_version.main_window.UserSessionModel import UserSessionModel


class FriendsListModel(QObject):
    def __init__(self):
        super().__init__()
        self.user_session = UserSessionModel()
        self.user_id = UserSessionModel().get_user_id()

    @error_catcher(log_func=logging.error, default_return=False)
    def get_friends(self, user_id, status='accepted'):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('get_friends_list_query'), (user_id, user_id, status))
                friends = cursor.fetchall()
                print('connection established.')
                return friends
        finally:
            if conn:
                self.user_session.release_connection(conn)
                print('connection released')

    @error_catcher(log_func=logging.error, default_return=False)
    def get_received_friend_requests(self, user_id):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('get_friend_requests_query'), (user_id,))
                requests = cursor.fetchall()
                print('connection established.')
                return requests
        finally:
            if conn:
                self.user_session.release_connection(conn)
                print('connection released')

    @error_catcher(log_func=logging.error, default_return=False)
    def accept_friend_request(self, user_id, friend_id):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('accept_friend_request_update_query'), (user_id, friend_id))

                if cursor.rowcount == 1:  # Only proceed if the update was successful
                    cursor.execute(self.user_session.get_query('accept_friend_request_reverse_query'), (user_id, friend_id))
                    print(f'Friend request from {user_id} was accepted by {friend_id}')
                    conn.commit()
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def reject_friend_request(self, user_id, friend_id):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('reject_friend_request_query'), (user_id, friend_id, friend_id, user_id))
                conn.commit()
                print(f"Friend request from user_id {user_id} to user_id {friend_id} has been rejected.")
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def username_to_userid(self, username):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('username_to_user_id_query'), (username,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the user_id
                else:
                    print("Username not found")
                    return None
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def send_friend_request(self, user_id, friend_id):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('send_friend_request_query'), (user_id, friend_id))
                conn.commit()
        finally:
            if conn:
                self.user_session.release_connection(conn)