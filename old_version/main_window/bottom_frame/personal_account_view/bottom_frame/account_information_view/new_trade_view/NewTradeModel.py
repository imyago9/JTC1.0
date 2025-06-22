import logging

import psycopg2
from PyQt5.QtCore import QObject

from old_version.utils import error_catcher

from old_version.main_window.UserSessionModel import UserSessionModel


class NewTradeModel(QObject):
    def __init__(self):
        super().__init__()
        self.user_session = UserSessionModel()

    @error_catcher(log_func=logging.error, default_return=False)
    def insert_trade(self, instrument, direction, entries, exits, entry_time, exit_time, profit, com):
        conn = None
        account_id = self.user_session.personal_account_session.get_current_account()
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO trades (account_id, instrument, direction, entry_time, exit_time, profit, com)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) 
                    RETURNING trade_id
                """, (account_id, instrument, direction, entry_time, exit_time, profit, com))

                trade_id = cursor.fetchone()[0]

                for entry_price, entry_qty in entries:
                    cursor.execute("""
                        INSERT INTO trade_entries (trade_id, entry_price, entry_qty)
                        VALUES (%s, %s, %s)
                    """, (trade_id, entry_price, entry_qty))

                for exit_price, exit_qty in exits:
                    cursor.execute("""
                        INSERT INTO trade_exits (trade_id, exit_price, exit_qty)
                        VALUES (%s, %s, %s)
                    """, (trade_id, exit_price, exit_qty))
                conn.commit()
                return trade_id
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def insert_zone_scoring(self, trade_id, scores):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO trade_zones (trade_id, strength, basetime, freshness, trend, curve, profitzone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (trade_id,
                      scores['strength'] if scores['strength'] is not None else int(0),
                      scores['basetime'] if scores['basetime'] is not None else float(0.0),
                      scores['freshness'] if scores['freshness'] is not None else int(0),
                      scores['trend'] if scores['trend'] is not None else int(0),
                      scores['curve'] if scores['curve'] is not None else float(0.0),
                      scores['profitzone'] if scores['profitzone'] is not None else int(0)))
                conn.commit()
                print(f'Inserting scoring into trade id: {trade_id}')
                return True
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def insert_screenshot(self, trade_id, screenshot_data, label):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO trade_screenshots (trade_id, screenshot, screenshot_index)
                VALUES (%s, %s, %s) RETURNING screenshot_id;
                """
                cursor.execute(insert_query, (trade_id, psycopg2.Binary(screenshot_data), label))
                screenshot_id = cursor.fetchone()[0]
                conn.commit()
                print(f'Inserting screenshot {label} into trade id: {trade_id}')
                return screenshot_id
        finally:
            if conn:
                self.user_session.release_connection(conn)

    def check_save_all_trade_information(self, trade_data, screenshots):
        try:
            # Save trade and get trade_id
            trade_id = self.insert_trade(
                trade_data['instrument'],
                trade_data['direction'],
                trade_data['entries'],
                trade_data['exits'],
                trade_data['entry_time'],
                trade_data['exit_time'],
                trade_data['profit'],
                trade_data['commission'],
            )

            self.insert_zone_scoring(trade_id, trade_data)

            for label, screenshot_data in screenshots:
                if screenshot_data:
                    self.insert_screenshot(trade_id, screenshot_data, label)
        except Exception as e:
            print(f"Error saving trade with screenshots: {e}")
