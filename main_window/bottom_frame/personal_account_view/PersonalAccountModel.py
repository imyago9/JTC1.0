import numpy as np
import pandas as pd
import logging

from PyQt5.QtCore import QDate, QObject

from main_window.UserSessionModel import UserSessionModel
from utils import error_catcher


class PersonalAccountModel(QObject):
    def __init__(self):
        super().__init__()
        self.user_session = UserSessionModel()
        self.personal_account_session = self.user_session.start_personal_account_session()

        self.user_id = self.user_session.get_user_id()

        self.data = None

    @error_catcher(log_func=logging.error, default_return=False)
    def check_account_money_visibility(self, account_id):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('check_account_money_visibility_query'), (account_id,))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    print('Error?')
                    return None
        finally:
            if conn:
                self.user_session.release_connection(conn)

    @error_catcher(log_func=logging.error, default_return=False)
    def get_trades_for_account(self, account_id):
        conn = None
        try:
            conn = self.user_session.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(self.user_session.get_query('get_trades_for_account_id_query'), (account_id,))
                trades = cursor.fetchall()
                trade_data = {}
                for row in trades:
                    trade_id = row[0]
                    if trade_id not in trade_data:
                        trade_data[trade_id] = {
                            'trade_id': trade_id,
                            'instrument': row[1],
                            'direction': row[2],
                            'entry_time': row[3],
                            'exit_time': row[4],
                            'profit': row[5],
                            'commission': row[6],
                            'entries': [],
                            'exits': [],
                            'strength': row[11],
                            'basetime': row[12],
                            'freshness': row[13],
                            'trend': row[14],
                            'curve': row[15],
                            'profitzone': row[16],
                        }
                    if row[7] is not None and row[8] is not None:
                        trade_data[trade_id]['entries'].append({'price': row[7], 'quantity': row[8]})
                    if row[9] is not None and row[10] is not None:
                        trade_data[trade_id]['exits'].append({'price': row[9], 'quantity': row[10]})
                return list(trade_data.values())
        finally:
            if conn:
                self.user_session.release_connection(conn)

    def fetchAccountData(self, account_id):
        try:
            trades = self.get_trades_for_account(account_id)
            if trades:
                self.data = self.tradesToDataframe(trades)
                self.user_session.personal_account_session.set_trade_data(self.data)
                return trades
        except Exception as e:
            print(f'Error fetching data: {e}')

    def getAccountDateRange(self):
        if self.data is None or not self.data.empty:
            return self.data['entry_time'].min(), self.data['exit_time'].max()
        else:
            return None, None

    def determineDateRange(self, start_date=None, end_date=None):
        try:
            if start_date and end_date:
                return pd.to_datetime(start_date), pd.to_datetime(end_date)
            else:
                return self.getAccountDateRange()
        except Exception as e:
            print(f'Error determining date range: {e}')

    def filterDataByDateRange(self, start_date, end_date):
        try:
            if self.data is None or self.data.empty:
                print('No data to filter')
                return pd.DataFrame()
            filtered_data = self.data[
                (self.data['exit_time'] >= pd.to_datetime(start_date)) &
                (self.data['exit_time'] <= pd.to_datetime(end_date))
                ]
            return filtered_data
        except Exception as e:
            print(f'Error filtering data by date range: {e}')

    @staticmethod
    def groupTradeData(filtered_data):
        try:
            data = filtered_data.groupby('entry_time').agg(
                profit=('profit', 'sum'),
                direction=('direction', 'first'),
                instrument=('instrument', 'first')
            ).reset_index()
            return data
        except Exception as e:
            print(f'Error grouping trade data: {e}')

    @staticmethod
    def assignTradeResults(data):
        try:
            data['result'] = data['profit'].apply(lambda p: 'L' if p < 0 else ('B' if p == 0 else 'W'))
            return data
        except Exception as e:
            print(f'Error assigning trade results: {e}')

    @staticmethod
    def calculateTradeStats(grouped_data):
        try:
            total_trades = len(grouped_data)
            win_trades = len(grouped_data[grouped_data['result'] == 'W'])
            loss_trades = len(grouped_data[grouped_data['result'] == 'L'])
            break_even_trades = len(grouped_data[grouped_data['result'] == 'B'])

            avg_win = grouped_data[grouped_data['result'] == 'W']['profit'].mean()
            avg_loss = grouped_data[grouped_data['result'] == 'L']['profit'].mean()
            net_pnl = grouped_data['profit'].sum()

            return {
                'total_trades': total_trades,
                'net_pnl': net_pnl,
                'win_rate': (win_trades / total_trades) * 100 if total_trades > 0 else 0,
                'loss_rate': (loss_trades / total_trades) * 100 if total_trades > 0 else 0,
                'break_even_rate': (break_even_trades / total_trades) * 100 if total_trades > 0 else 0,
                'avg_win': avg_win if not pd.isna(avg_win) else 0,
                'avg_loss': avg_loss if not pd.isna(avg_loss) else 0,
                'avg_rr': avg_win / np.abs(avg_loss) if avg_loss else 0,
            }
        except Exception as e:
            print(f'Error calculating trade stats: {e}')

    @staticmethod
    def tradesToDataframe(trades):
        try:
            df = pd.DataFrame(trades)
            df['entry_time'] = pd.to_datetime(df['entry_time'])
            df['exit_time'] = pd.to_datetime(df['exit_time'])
            return df
        except Exception as e:
            print(f'Error converting trades to dataframe: {e}')

    def isDataAvailable(self):
        return (self.data is not None
                and not self.data.empty)



