import os
import random
import smtplib
from email.message import EmailMessage

import bcrypt
import logging
from PyQt5.QtCore import QObject
from utils import error_catcher
from db_connection import db_connection


class AuthService(QObject):

    def __init__(self):
        super().__init__()
        self.db_conn = db_connection()
        self.otp = None

    @staticmethod
    def hash_password(password):
        """Hash a plaintext password."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed_password):
        """Verify a plaintext password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @error_catcher(log_func=logging.error, default_return=False)
    def verify_credentials(self, username, password):
        conn = None
        try:
            conn = self.db_conn.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.db_conn.get_query('verify_credentials_query'), (username, username))
                result = cursor.fetchone()
                if result:
                    user_id, stored_hash_pass = result
                    if self.check_password(password, stored_hash_pass):
                        print('User ID in current session:', result[0])
                        return True, user_id
                    else:
                        print('Password does not match.')
                        return False, None
                else:
                    print('User not found.')
                    return False, None

        finally:
            self.db_conn.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def register_user(self, email, username, password):
        conn = None
        try:
            conn = self.db_conn.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.db_conn.get_query('create_user_query'), (username,
                                                                             self.hash_password(password),
                                                                             email))
                user_id = cursor.fetchone()[0]
                conn.commit()
                return user_id
        finally:
            self.db_conn.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def check_if_identifier_exists(self, username):
        conn = None
        try:
            conn = self.db_conn.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.db_conn.get_query('check_if_identifier_exists_query'), (username, username))
                return cursor.fetchone()[0]
        finally:
            self.db_conn.release_connection(conn)

    def update_password(self, email, password):
        conn = None
        try:
            conn = self.db_conn.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.db_conn.get_query('change_password_query'), (self.hash_password(password), email))
                conn.commit()
        finally:
            self.db_conn.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def send_otp(self, to_email):
        # Replace these with your sender email credentials
        sender_email = "yagofarhat555@gmail.com"
        sender_password = "hdxj tipa cghz qdga"

        # Generate a 6-digit OTP
        self.otp = self.create_otp()

        # Create the email message
        msg = EmailMessage()
        msg.set_content(f"Your OTP is: {self.otp}")
        msg['Subject'] = "Your OTP Verification Code"
        msg['From'] = sender_email
        msg['To'] = to_email

        # Connect to the SMTP server (using Gmail's SMTP server as an example)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Secure the connection
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print("OTP sent successfully!")
        except Exception as e:
            print(f"An error occurred while sending the OTP: {e}")
            raise

    @staticmethod
    def create_otp():
        return random.randint(100000, 999999)
