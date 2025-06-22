from PyQt5.QtCore import QObject, pyqtSignal, QDate
import pandas as pd


class CalendarViewModel(QObject):
    error_occurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_date = QDate.currentDate()
        self.full_data = pd.DataFrame()
        self.filtered_data = pd.DataFrame()

    def populate_calendar(self, each_day_label):
        """Populate the calendar with the correct day placement for the current month."""
        year, month = self.current_date.year(), self.current_date.currentDate().month()
        date = QDate(year, month, 1)
        day_of_week = date.dayOfWeek() - 1
        row = 1
        col = day_of_week

        while date.month() == month:
            if col < 7:
                each_day_label[(row, col)][0].setText(str(date.day()))
                col += 1
            date = date.addDays(1)
            if col >= 7:
                col = 0
                row += 1

    def clear_calendar(self, each_day_label):
        try:
            for (row, col), (date_label, profit_label, trades_label) in each_day_label.items():
                date_label.setText("")
                profit_label.setText("")
                trades_label.setText("")
        except Exception as e:
            self.error_occurred.emit(f"Failed to clear calendar: {e}")

    def get_colored_text(self, day):
        """Get the color and details for a specific day."""
        try:
            date_to_check = QDate(self.current_date.year(), self.current_date.month(), day).toString("yyyy-MM-dd")
            if self.filtered_data.empty:
                return 0, 0
            else:
                day_data = self.filtered_data[self.filtered_data['entry_time'].dt.strftime('%Y-%m-%d') == date_to_check]
                profit = day_data['profit'].sum()
                trades = len(day_data)
            return profit, trades
        except Exception as e:
            self.error_occurred.emit(f"Failed to get day details: {e}")
            return 0, 0

    def populate_calendar(self, each_day_label):
        """Populate the calendar with the correct day placement for the current month."""
        year, month = self.current_date.year(), self.current_date.month()
        date = QDate(year, month, 1)
        day_of_week = date.dayOfWeek() - 1
        row, col = 1, day_of_week

        self.clear_calendar(each_day_label)

        while date.month() == month:
            # Populate the calendar cell
            each_day_label[(row, col)][0].setText(str(date.day()))  # Day number
            each_day_label[(row, col)][0].setStyleSheet("""color: white; border: none;""")  # Default style
            col += 1

            if col >= 7:  # Move to the next row if at the end of the week
                col = 0
                row += 1

            date = date.addDays(1)  # Increment to the next day

    def setColoredText(self, day, profit, trades, each_day_label):
        try:
            for (row, col), (date_label, profit_label, trades_label) in each_day_label.items():
                if date_label.text() == str(day):
                    if trades == 0:
                        date_label.setStyleSheet("color: #8f7b7b; border: none;")
                    else:
                        profit_color = '#c3dc9b' if int(profit) > 0 else ('#ff4c4c' if int(profit) < 0 else 'white')
                        profit = abs(profit)  # if self.money_visible else '---'
                        date_label.setText(str(day))
                        date_label.setStyleSheet("color: white; border: none;")
                        profit_label.setText(f'{profit}')
                        profit_label.setStyleSheet(f"color: {profit_color}; font-weight: bold; border: none;")
                        trades_label.setText(f"{trades}'Ts")
                        trades_label.setStyleSheet("color: white; border: none;")
                    break
        except Exception as e:
            self.error_occurred.emit(f"Failed to set colored text: {e}")

    def getAccountDateRange(self):
        try:
            if self.full_data is None or self.full_data.empty:
                return None, None
            else:
                return self.full_data['entry_time'].min(), self.full_data['exit_time'].max()
        except Exception as e:
            self.error_occurred.emit(f"Failed to get account date range: {e}")

    @staticmethod
    def convertToQDate(start_date, end_date):
        s_date = QDate(start_date.year, start_date.month, start_date.day)
        e_date = QDate(end_date.year, end_date.month, end_date.day)
        print(s_date, e_date)
        return s_date, e_date

    def filter_data_for_month(self, data):
        """Filter data for the current month."""
        try:
            if data is not None:
                data = pd.DataFrame(data)
                data['entry_time'] = pd.to_datetime(data['entry_time'])
                data['exit_time'] = pd.to_datetime(data['exit_time'])
                self.full_data = data
                self.filtered_data = data[data['entry_time'].dt.month == self.current_date.month()]
            else:
                self.filtered_data = pd.DataFrame()
        except Exception as e:
            self.error_occurred.emit(f"Failed to filter data: {e}")

    def navigate_month(self, direction):
        """Navigate to the next or previous month."""
        try:
            self.current_date = self.current_date.addMonths(direction)
            self.parent().update_graph(self.full_data)
        except Exception as e:
            self.error_occurred.emit(f"Failed to navigate calendar: {e}")
