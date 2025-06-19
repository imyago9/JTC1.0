from PyQt5.QtCore import QDateTime, pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, \
    QPushButton, QDateTimeEdit
from main_window.bottom_frame.personal_account_view.bottom_frame.z_utility.image_drop import ImageDropArea
from main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.new_trade_view.NewTradeViewModel import \
    NewTradeViewModel


class NewTradeView(QFrame):
    trade_created = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = NewTradeViewModel(self)

        self.layout = QHBoxLayout()

        self.setup_left_side()
        self.setup_right_side()

        self.entry_price_entries = [self.entry_price_entry]
        self.entry_quantity_entries = [self.entry_quantity_entry]
        self.exit_price_entries = [self.exit_price_entry]
        self.exit_quantity_entries = [self.exit_quantity_entry]

        self.layout.addWidget(self.left_side_frame)
        self.layout.addWidget(self.right_side_frame)

        self.set_current_datetime()
        self.setLayout(self.layout)

    def set_return_button_visible(self, status):
        self.return_button.setVisible(status)

    def setup_left_side(self):
        self.left_side_frame = QFrame()
        self.left_side_layout = QVBoxLayout(self.left_side_frame)

        self.return_button = QPushButton('Return', clicked=self.parent().displayThreeGraphView)

        self.instrument_label = QLabel('Instrument:')
        self.instrument_entry = QLineEdit()
        self.instrument_entry.setPlaceholderText('Ex: ES, NQ, etc..')

        self.direction_label = QLabel('Direction:')
        self.direction_entry = QComboBox()
        self.direction_entry.addItems(['Long', 'Short'])

        self.entry_price_quantity_label = QLabel('Entry Price & Qty')

        self.entry_price_quantity_frame = QFrame()
        self.entry_price_quantity_layout = QVBoxLayout(self.entry_price_quantity_frame)

        self.entry_price_quantity_row_frame = QFrame()
        self.entry_price_quantity_row_layout = QHBoxLayout(self.entry_price_quantity_row_frame)

        self.entry_price_entry = QDoubleSpinBox()
        self.entry_price_entry.setRange(0, 1000000)
        self.entry_price_entry.setDecimals(2)
        self.entry_price_quantity_row_layout.addWidget(self.entry_price_entry)

        self.entry_quantity_entry = QSpinBox()
        self.entry_quantity_entry.setRange(1, 1000000)
        self.entry_price_quantity_row_layout.addWidget(self.entry_quantity_entry)

        self.add_entry_price_quantity_slot = QPushButton('+', clicked=self.add_entry_price_quantity_row)
        self.entry_price_quantity_row_layout.addWidget(self.add_entry_price_quantity_slot)

        self.entry_price_quantity_layout.addWidget(self.entry_price_quantity_row_frame)

        self.exit_price_quantity_label = QLabel('Exit Price & Qty')

        self.exit_price_quantity_frame = QFrame()
        self.exit_price_quantity_layout = QVBoxLayout(self.exit_price_quantity_frame)

        self.exit_price_quantity_row_frame = QFrame()
        self.exit_price_quantity_row_layout = QHBoxLayout(self.exit_price_quantity_row_frame)

        self.exit_price_entry = QDoubleSpinBox()
        self.exit_price_entry.setRange(0, 1000000)
        self.exit_price_entry.setDecimals(2)
        self.exit_price_quantity_row_layout.addWidget(self.exit_price_entry)

        self.exit_quantity_entry = QSpinBox()
        self.exit_quantity_entry.setRange(1, 1000000)
        self.exit_price_quantity_row_layout.addWidget(self.exit_quantity_entry)

        self.add_exit_price_quantity_slot = QPushButton('+', clicked=self.add_exit_price_quantity_row)
        self.exit_price_quantity_row_layout.addWidget(self.add_exit_price_quantity_slot)
        self.exit_price_quantity_layout.addWidget(self.exit_price_quantity_row_frame)

        self.entry_time_label = QLabel('First entry time:')
        self.entry_time_entry = QDateTimeEdit()
        self.entry_time_entry.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.entry_time_entry.setCalendarPopup(True)

        self.exit_time_label = QLabel('Last exit time:')
        self.exit_time_entry = QDateTimeEdit()
        self.exit_time_entry.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.exit_time_entry.setCalendarPopup(True)

        self.profit_label = QLabel('Profit:')
        self.profit_entry = QDoubleSpinBox()
        self.profit_entry.setRange((-100000), 1000000)
        self.profit_entry.setDecimals(2)

        self.commission_label = QLabel('Commission:')
        self.commission_entry = QDoubleSpinBox()
        self.commission_entry.setRange(0, 1000000)
        self.commission_entry.setDecimals(2)

        widgets = [self.return_button, self.instrument_label, self.instrument_entry, self.direction_label,
                   self.direction_entry, self.entry_price_quantity_label, self.entry_price_quantity_frame,
                   self.exit_price_quantity_label, self.exit_price_quantity_frame, self.entry_time_label,
                   self.entry_time_entry, self.exit_time_label, self.exit_time_entry, self.profit_label,
                   self.profit_entry, self.commission_label, self.commission_entry]

        for widget in widgets:
            self.left_side_layout.addWidget(widget)

    def setup_right_side(self):
        self.screenshots_frame = QFrame()
        self.screenshots_layout = QVBoxLayout(self.screenshots_frame)

        self.htf_screenshot_label = QLabel('HTF SS:')
        self.htf_screenshot_row = ImageDropArea()

        self.itf_screenshot_label = QLabel('ITF SS:')
        self.itf_screenshot_row = ImageDropArea()

        self.ltf_screenshot_label = QLabel('LTF SS:')
        self.ltf_screenshot_row = ImageDropArea()

        self.screenshots_layout.addWidget(self.htf_screenshot_label)
        self.screenshots_layout.addWidget(self.htf_screenshot_row)
        self.screenshots_layout.addWidget(self.itf_screenshot_label)
        self.screenshots_layout.addWidget(self.itf_screenshot_row)
        self.screenshots_layout.addWidget(self.ltf_screenshot_label)
        self.screenshots_layout.addWidget(self.ltf_screenshot_row)

        self.strength_entry = QComboBox()
        self.strength_entry.addItem('Strength')
        self.strength_entry.addItems(['0', '1', '2'])
        self.strength_entry.setCurrentIndex(0)
        self.strength_entry.model().item(0).setEnabled(False)

        self.basetime_entry = QComboBox()
        self.basetime_entry.addItem('Base Time')
        self.basetime_entry.addItems(['0', '0.5', '1'])
        self.basetime_entry.setCurrentIndex(0)
        self.basetime_entry.model().item(0).setEnabled(False)

        self.freshness_entry = QComboBox()
        self.freshness_entry.addItem('Freshness')
        self.freshness_entry.addItems(['0', '1', '2'])
        self.freshness_entry.setCurrentIndex(0)
        self.freshness_entry.model().item(0).setEnabled(False)

        self.trend_entry = QComboBox()
        self.trend_entry.addItem('Trend')
        self.trend_entry.addItems(['0', '1', '2'])
        self.trend_entry.setCurrentIndex(0)
        self.trend_entry.model().item(0).setEnabled(False)

        self.curve_entry = QComboBox()
        self.curve_entry.addItem('Curve')
        self.curve_entry.addItems(['0', '0.5', '1'])
        self.curve_entry.setCurrentIndex(0)
        self.curve_entry.model().item(0).setEnabled(False)

        self.profit_zone_entry = QComboBox()
        self.profit_zone_entry.addItem('Profit Zone')
        self.profit_zone_entry.addItems(['0', '1', '2'])
        self.profit_zone_entry.setCurrentIndex(0)
        self.profit_zone_entry.model().item(0).setEnabled(False)

        self.right_side_frame = QFrame()
        self.right_side_layout = QVBoxLayout(self.right_side_frame)

        widgets = [self.screenshots_frame, self.strength_entry, self.basetime_entry, self.freshness_entry,
                   self.trend_entry, self.curve_entry, self.profit_zone_entry]

        for widget in widgets:
            self.right_side_layout.addWidget(widget)

        self.create_trade_button = QPushButton('Create Trade', clicked=self.create_trade)
        self.clear_button = QPushButton('Clear All', clicked=self.clear_fields)

        self.right_side_layout.addWidget(self.clear_button)
        self.right_side_layout.addWidget(self.create_trade_button)

    def add_entry_price_quantity_row(self):
        try:
            entry_price_quantity_row_frame = QFrame()
            entry_price_quantity_row_layout = QHBoxLayout(entry_price_quantity_row_frame)

            entry_price_entry = QDoubleSpinBox()
            entry_price_entry.setRange(0, 1000000)
            entry_price_entry.setDecimals(2)
            entry_price_quantity_row_layout.addWidget(entry_price_entry)

            entry_quantity_entry = QSpinBox()
            entry_quantity_entry.setRange(1, 1000000)
            entry_price_quantity_row_layout.addWidget(entry_quantity_entry)

            delete_button = QPushButton('-')
            delete_button.clicked.connect(
                lambda: self.delete_entry_row(entry_price_quantity_row_frame, entry_price_entry, entry_quantity_entry))
            entry_price_quantity_row_layout.addWidget(delete_button)

            self.entry_price_quantity_layout.addWidget(entry_price_quantity_row_frame)

            self.entry_price_entries.append(entry_price_entry)
            self.entry_quantity_entries.append(entry_quantity_entry)

        except Exception as e:
            print(f'Failed to add entry price quantity row: {e}')

    def add_exit_price_quantity_row(self):
        try:
            exit_price_quantity_row_frame = QFrame()
            exit_price_quantity_row_layout = QHBoxLayout(exit_price_quantity_row_frame)

            exit_price_entry = QDoubleSpinBox()
            exit_price_entry.setRange(0, 1000000)
            exit_price_entry.setDecimals(2)
            exit_price_quantity_row_layout.addWidget(exit_price_entry)

            exit_quantity_entry = QSpinBox()
            exit_quantity_entry.setRange(1, 1000000)
            exit_price_quantity_row_layout.addWidget(exit_quantity_entry)

            delete_button = QPushButton('-')
            delete_button.clicked.connect(
                lambda: self.delete_exit_row(exit_price_quantity_row_frame, exit_price_entry, exit_quantity_entry))
            exit_price_quantity_row_layout.addWidget(delete_button)

            self.exit_price_quantity_layout.addWidget(exit_price_quantity_row_frame)

            self.exit_price_entries.append(exit_price_entry)
            self.exit_quantity_entries.append(exit_quantity_entry)

        except Exception as e:
            print(f'Failed to add exit price quantity row: {e}')

    def delete_entry_row(self, row_frame, entry_price_entry, entry_quantity_entry):
        try:
            self.entry_price_quantity_layout.removeWidget(row_frame)
            row_frame.deleteLater()
            self.entry_price_entries.remove(entry_price_entry)
            self.entry_quantity_entries.remove(entry_quantity_entry)
        except Exception as e:
            print(f'Failed to delete entry price quantity row: {e}')

    def delete_exit_row(self, row_frame, exit_price_entry, exit_quantity_entry):
        try:
            self.exit_price_quantity_layout.removeWidget(row_frame)
            row_frame.deleteLater()
            self.exit_price_entries.remove(exit_price_entry)
            self.exit_quantity_entries.remove(exit_quantity_entry)
        except Exception as e:
            print(f'Failed to delete exit price quantity row: {e}')

    def create_trade(self):
        try:
            instrument = self.instrument_entry.text()
            direction = self.direction_entry.currentText()

            entries = []
            for price_entry, quantity_entry in zip(self.entry_price_entries, self.entry_quantity_entries):
                entry_price = price_entry.value()
                entry_quantity = quantity_entry.value()
                entries.append((entry_price, entry_quantity))

            exits = []
            for price_entry, quantity_entry in zip(self.exit_price_entries, self.exit_quantity_entries):
                exit_price = price_entry.value()
                exit_quantity = quantity_entry.value()
                exits.append((exit_price, exit_quantity))

            entry_time = self.entry_time_entry.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            exit_time = self.exit_time_entry.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            profit = self.profit_entry.value()
            commission = self.commission_entry.value()
            strength = int(self.strength_entry.currentText())
            basetime = float(self.basetime_entry.currentText())
            freshness = int(self.freshness_entry.currentText())
            trend = int(self.trend_entry.currentText())
            curve = float(self.curve_entry.currentText())
            profit_zone = int(self.profit_zone_entry.currentText())

            # Check if all fields are filled out
            if not all([instrument, direction, entries, exits, entry_time, exit_time, profit]):
                print(
                    f"All fields must be filled out. {instrument}, {direction}, {entries}, {exits}, {entry_time}, {exit_time}, {profit}, {commission}, {strength}, {basetime}, {freshness}, {trend}, {curve}, {profit_zone}")
                return

            screenshots = []
            for label, screenshot_row in zip(['HTF', 'ITF', 'LTF'], [self.htf_screenshot_row, self.itf_screenshot_row,
                                                                     self.ltf_screenshot_row]):
                screenshot_name = screenshot_row.line_edit.text()
                if screenshot_name != "Drop an image here":
                    screenshot_row.get_file_path()
                    screenshot_path = screenshot_row.get_file_path()
                    try:
                        with open(screenshot_path, 'rb') as file:
                            screenshot_data = file.read()
                            screenshots.append((label, screenshot_data))
                    except Exception as e:
                        print(f"Failed to read screenshot {screenshot_name}: {e}")
                        return
            trade_data = {
                "instrument": instrument,
                "direction": direction,
                "entries": entries,
                "exits": exits,
                "entry_time": entry_time,
                "exit_time": exit_time,
                "profit": profit,
                "commission": commission,
                "strength": strength,
                "basetime": basetime,
                "freshness": freshness,
                "trend": trend,
                "curve": curve,
                "profitzone": profit_zone
            }
            self.view_model.check_save_all_trade_information(trade_data, screenshots)
            self.trade_created.emit()
        except Exception as e:
            print(f'Failed to send trade database: {e}')

    def clear_fields(self):
        self.instrument_entry.clear()
        self.direction_entry.setCurrentIndex(0)
        self.entry_price_entries = [self.entry_price_entry]
        self.entry_quantity_entries = [self.entry_quantity_entry]
        self.exit_price_entries = [self.exit_price_entry]
        self.exit_quantity_entries = [self.exit_quantity_entry]
        self.entry_price_quantity_layout.addWidget(self.entry_price_quantity_row_frame)
        self.exit_price_quantity_layout.addWidget(self.exit_price_quantity_row_frame)
        self.set_current_datetime()
        self.profit_entry.setValue(0)
        self.commission_entry.setValue(0)
        self.strength_entry.setCurrentIndex(0)
        self.basetime_entry.setCurrentIndex(0)
        self.freshness_entry.setCurrentIndex(0)
        self.trend_entry.setCurrentIndex(0)
        self.curve_entry.setCurrentIndex(0)
        self.profit_zone_entry.setCurrentIndex(0)

    def set_current_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        self.entry_time_entry.setDateTime(current_datetime)
        self.exit_time_entry.setDateTime(current_datetime)
