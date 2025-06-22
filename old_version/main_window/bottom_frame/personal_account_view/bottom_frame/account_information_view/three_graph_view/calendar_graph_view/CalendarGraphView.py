import pandas as pd
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QDateEdit, \
    QLabel, QPushButton, QSizePolicy, QFrame

from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.calendar_graph_view.CalendarGraphViewModel import \
    CalendarViewModel


class CalendarGraphWidget(QWidget):
    day_clicked = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = CalendarViewModel(self)

        self.each_day_label = {}
        self.layout = QVBoxLayout(self)
        self.init_dateedits()
        self.init_navigation()
        self.initUI()
        self.init_bindings()

    def init_dateedits(self):
        self.date_edit_layout = QHBoxLayout()
        self.fde = QDateEdit()
        self.fde.setCalendarPopup(True)
        self.sde = QDateEdit()
        self.sde.setCalendarPopup(True)
        self.date_edit_layout.addStretch()
        sd_label = QLabel('Start Date')
        sd_label.setStyleSheet('border: none; color: white;')
        ed_label = QLabel('End Date')
        ed_label.setStyleSheet('border: none; color: white;')
        self.date_edit_layout.addWidget(sd_label)
        self.date_edit_layout.addWidget(self.fde)
        self.date_edit_layout.addWidget(self.sde)
        self.date_edit_layout.addWidget(ed_label)
        self.date_edit_layout.addStretch()

        self.layout.addLayout(self.date_edit_layout)

    def init_navigation(self):
        self.navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("<", self)
        self.navigation_layout.addWidget(self.prev_button)

        self.current_month_label = QLabel(self)
        self.current_month_label.setStyleSheet('border: none; color: white;')
        self.navigation_layout.addWidget(self.current_month_label)

        self.next_button = QPushButton(">", self)
        self.navigation_layout.addWidget(self.next_button)
        self.layout.addLayout(self.navigation_layout)

    def initUI(self):
        try:
            self.calendar_layout = QGridLayout()
            days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", 'Sun']

            for i, day in enumerate(days_of_week):
                day_label = QLabel(day)
                day_label.setStyleSheet('border: none; color: white;')
                day_label.setAlignment(Qt.AlignCenter)
                day_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.calendar_layout.addWidget(day_label, 0, i)

            for row in range(1, 7):
                self.calendar_layout.setRowStretch(row, 1)
                for col in range(7):
                    each_day_frame = ClickableFrame(self)
                    date_label, profit_value_label, trade_number_label = each_day_frame.get_labels()

                    self.calendar_layout.addWidget(each_day_frame, row, col)

                    self.each_day_label[(row, col)] = (date_label, profit_value_label, trade_number_label)
                    self.calendar_layout.setColumnStretch(col, 1)

            self.layout.addLayout(self.calendar_layout)
        except Exception as e:
            print(f'Error initializing UI: {e}')

    def init_bindings(self):
        self.view_model.error_occurred.connect(self.show_error)
        self.prev_button.clicked.connect(lambda: self.view_model.navigate_month(-1))
        self.next_button.clicked.connect(lambda: self.view_model.navigate_month(1))

    def update_graph(self, data):
        try:
            self.view_model.filter_data_for_month(data)
            self.current_month_label.setText(f"{self.view_model.current_date.toString('MMMM yyyy')}")
            self.view_model.populate_calendar(self.each_day_label)
            self.updateDateEdit()
            for day in range(1, self.view_model.current_date.daysInMonth() + 1):
                profit, trades = self.view_model.get_colored_text(day)
                self.view_model.setColoredText(day, profit, trades, self.each_day_label)
            print('Calendar updated')
        except Exception as e:
            print(f'Failed to update calendar: {e}')

    @staticmethod
    def show_error(e):
        print(f'An error occurred: {e}')

    def wheelEvent(self, event):
        # Check the direction of the scroll
        if event.angleDelta().y() > 0:
            self.view_model.navigate_month(-1)
        else:
            self.view_model.navigate_month(1)

    def disableCalendarDateEdits(self):
        for i in [self.fde, self.sde]:
            i.setEnabled(False)
            i.clearMaximumDate()
            i.clearMinimumDate()
            i.blockSignals(True)

    def configureDEDates(self, start_date=None, end_date=None):
        try:
            account_first_date, account_last_date = self.view_model.getAccountDateRange()
            account_start_date, account_end_date = self.view_model.convertToQDate(account_first_date,
                                                                                  account_last_date)
            for calendar_date_edit in [self.fde, self.sde]:
                calendar_date_edit.setMinimumDate(account_start_date)
                calendar_date_edit.setMaximumDate(account_end_date)
                calendar_date_edit.blockSignals(False)
                calendar_date_edit.setEnabled(True)
            if start_date and end_date:
                print('DATES AHVE BEEN SELECTED.')
                start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
                selected_start_date, selected_end_date = self.view_model.convertToQDate(start_date, end_date)
                self.fde.setDate(selected_start_date)
                self.sde.setDate(selected_end_date)
            else:
                print('Dates have not been selected.')
                self.fde.setDate(account_start_date)
                self.sde.setDate(account_end_date)
        except Exception as e:
            print(f'Error configuring date edits: {e}')

    def updateDateEdit(self, start_date=None, end_date=None):
        try:
            self.disableCalendarDateEdits()
            self.configureDEDates(start_date=start_date, end_date=end_date)
        except Exception as e:
            print(f'Error updating date edit: {e}')


class ClickableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.date_label = QLabel("")
        self.date_label.setStyleSheet("border: none;")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.profit_value = QLabel("")
        self.profit_value.setStyleSheet("border: none;")
        self.profit_value.setAlignment(Qt.AlignCenter)
        self.profit_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.trade_number = QLabel("")
        self.trade_number.setStyleSheet("border: none;")
        self.trade_number.setAlignment(Qt.AlignCenter)
        self.trade_number.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.date_label)
        layout.addWidget(self.profit_value)
        layout.addWidget(self.trade_number)
        self.setLayout(layout)

    def get_labels(self):
        return self.date_label, self.profit_value, self.trade_number

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        try:
            parent = self.parent()
            print('pressed')
            # .day_clicked.emit(parent.account_id,str(f'{parent.current_date.year()}-
            # {parent.current_date.month():02d}-{int(self.date_label.text()):02d}'))
        except Exception as e:
            print(f'Failed mouse press event: {e}')
