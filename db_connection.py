import os
from psycopg2 import pool
from dotenv import load_dotenv
import logging

from utils import resource_path, error_catcher

load_dotenv(resource_path('resources/dot-envs/parameters.env'))
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

load_dotenv(resource_path('resources/dot-envs/sql-commands.env'))
queries = {
    "create_user_query": os.getenv('CREATE_USER_QUERY'),
    "change_password_query": os.getenv('CHANGE_PASSWORD_QUERY'),
    "verify_credentials_query": os.getenv('VERIFY_CREDENTIALS_QUERY'),
    "username_to_user_id_query": os.getenv('USERNAME_TO_USER_ID_QUERY'),
    "get_friends_list_query": os.getenv('GET_FRIENDS_LIST_QUERY'),
    "get_friend_requests_query": os.getenv('GET_FRIEND_REQUESTS_QUERY'),
    "accept_friend_request_update_query": os.getenv('ACCEPT_FRIEND_REQUEST_UPDATE_QUERY'),
    "accept_friend_request_reverse_query": os.getenv('ACCEPT_FRIEND_REQUEST_REVERSE_QUERY'),
    "reject_friend_request_query": os.getenv('REJECT_FRIEND_REQUEST_QUERY'),
    "send_friend_request_query": os.getenv('SEND_FRIEND_REQUEST_QUERY'),
    "get_trades_for_account_id_query": os.getenv('GET_TRADES_FOR_ACCOUNT_ID_QUERY'),
    "check_account_money_visibility_query": os.getenv('CHECK_ACCOUNT_MONEY_VISIBILITY_QUERY'),
    "select_accounts_from_type_query": os.getenv('SELECT_ACCOUNTS_FROM_TYPE_QUERY'),
    "select_all_accounts_query": os.getenv('SELECT_ALL_ACCOUNTS_QUERY'),
    "insert_new_account_query": os.getenv('INSERT_NEW_ACCOUNT_QUERY'),
    "check_if_identifier_exists_query": os.getenv('CHECK_IF_IDENTIFIER_EXISTS')
}


class db_connection:
    def __init__(self):
        self.connection_pool = connection_pool

    @staticmethod
    @error_catcher(log_func=logging.error, default_return=False)
    def get_connection():
        """Retrieve a connection from the pool."""
        conn = connection_pool.getconn()
        return conn

    @staticmethod
    def release_connection(conn):
        """Release a connection back to the pool."""
        connection_pool.putconn(conn)

    @staticmethod
    def get_query(query_name):
        return queries[query_name]

