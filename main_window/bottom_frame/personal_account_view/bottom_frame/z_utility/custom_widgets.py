from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from main_window.mySQL.SqlModel import get_trade_note, insert_daily_note, update_trade_note


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
            parent.day_clicked.emit(parent.account_id,
                                    str(f'{parent.current_date.year()}-{parent.current_date.month():02d}-{int(self.date_label.text()):02d}'))
        except Exception as e:
            print(f'Failed mouse press event: {e}')


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type = type
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        try:
            if self.pixmap() is not None:
                self.parent().set_screenshot_first_stack()
        except Exception as e:
            print(f'Failed mouse press event: {e}')


class LimitedTextEdit(QTextEdit):
    def __init__(self, char_limit, *args, **kwargs):
        super(LimitedTextEdit, self).__init__(*args, **kwargs)
        self.char_limit = char_limit

    def keyPressEvent(self, event):
        if len(self.toPlainText()) >= self.char_limit and event.key() not in (Qt.Key_Backspace, Qt.Key_Delete):
            # Ignore the key press if the character limit is reached
            event.ignore()
        else:
            super(LimitedTextEdit, self).keyPressEvent(event)

    def insertFromMimeData(self, source):
        # Also handle paste operations
        if len(self.toPlainText()) + len(source.text()) > self.char_limit:
            return
        super(LimitedTextEdit, self).insertFromMimeData(source)


class CustomNoteView(QWidget):
    go_back_button_pressed = pyqtSignal()

    def __init__(self, parent=None, trade_id=None, account_id=None, date=None, type=None):
        super(CustomNoteView, self).__init__(parent)
        self.trade_id = trade_id
        self.account_id = account_id
        self.note_date = date
        self.first_date = None
        self.second_date = None
        if self.trade_id:
            self.server_note_id, self.server_note, self.server_created_at = get_trade_note(trade_id=trade_id)
        if self.account_id and self.note_date:
            self.server_note_id, self.server_note, self.server_created_at = get_trade_note(account_id=account_id,
                                                                                           date=date)

        self.setupView()
        if self.server_note is not None:
            self.notes_entry_box.setText(str(self.server_note))
            self.notes_entry_box.setStyleSheet("""
            QWidget {
                background-color: #222222;
                color: white;
                border: none;
                outline: none;
            }
        """)
        self.setStyleSheet("""
            QWidget {
                background-color: #222222;
                color: white;
            }
        """)

    def setTitle(self):
        title_label = f'Trade Notes:\n' if self.trade_id else f'Daily Notes:\n' if self.account_id else ""
        self.title.setText(title_label)
        self.title.setStyleSheet('color: white;')

    def setupView(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.notes_frame = QFrame()
        self.notes_layout = QVBoxLayout(self.notes_frame)
        self.title = QLabel()
        self.setTitle()
        self.title.setAlignment(Qt.AlignCenter)
        self.notes_entry_box = LimitedTextEdit(char_limit=500)
        if self.account_id:
            def confirm_pressed():
                try:
                    self.save_button.setText('Save Daily Note')
                    self.save_button.disconnect()
                    self.save_button.clicked.connect(save_button_pressed)

                    self.go_back_button.setText('Go Back')
                    self.go_back_button.disconnect()
                    self.go_back_button.clicked.connect(emit_back_signal)
                    if self.server_note_id:
                        self.setTitle()
                        update_trade_note(self.server_note_id, self.notes_entry_box.toPlainText(), note_type='daily')
                    else:
                        insert_daily_note(self.account_id, self.notes_entry_box.toPlainText(), self.note_date)
                    self.notes_entry_box.setStyleSheet("""
                        QWidget {
                            background-color: #222222;
                            color: white;
                            border: none;
                            outline: none;
                        }
                    """)
                except Exception as e:
                    print(f'Failed to press confirm button: {e}')

            def cancel_pressed():
                self.save_button.setText('Save Daily Note')
                self.save_button.disconnect()
                self.save_button.clicked.connect(save_button_pressed)

                self.go_back_button.setText('Go Back')
                self.go_back_button.disconnect()
                self.go_back_button.clicked.connect(emit_back_signal)
                if self.server_note_id:
                    self.setTitle()

            def save_button_pressed():
                try:
                    self.save_button.setText('Confirm')
                    self.save_button.disconnect()
                    self.save_button.clicked.connect(confirm_pressed)
                    self.go_back_button.setText('Cancel')
                    self.go_back_button.disconnect()
                    self.go_back_button.clicked.connect(cancel_pressed)
                    if self.server_note_id:
                        self.title.setText('Replace existing note?')
                        self.title.setStyleSheet('color: #ff4c4c;')
                except Exception as e:
                    print(f'Failed to press save button: {e}')

            def emit_back_signal():
                try:
                    self.go_back_button_pressed.emit()
                except Exception as e:
                    print(f'Failed to emit back signal: {e}')

            self.go_back_button = QPushButton('Go Back', clicked=emit_back_signal)
            self.go_back_button.setStyleSheet("""
                        QPushButton:hover {
                            background-color: #ff4c4c;
                        }
                        QPushButton {
                            border: 2px solid #ff7f7f;
                        }""")

            self.notes_layout.addWidget(self.go_back_button)
            self.save_button = QPushButton('Save Daily Note', clicked=save_button_pressed)
            self.save_button.setStyleSheet("""
                        QPushButton:hover {
                            background-color: #2c7e33;
                        }""")
            self.notes_layout.addWidget(self.save_button)
        self.notes_layout.addWidget(self.title)
        self.notes_layout.addWidget(self.notes_entry_box)
        layout.addWidget(self.notes_frame)
        if self.server_note:
            self.notes_entry_box.setText(self.server_note)

    def get_note_text(self):
        return self.notes_entry_box.toPlainText()


def group_trades_by_entry_time(data):
    # Group by entry_time
    grouped_data = data.groupby('entry_time').agg(
        {
            'exit_time': 'last',  # Take the last exit time
            'instrument': 'first',  # Assuming all rows have the same instrument, take the first
            'direction': 'first',  # Assuming direction is the same, take the first
            'entry_price': lambda x: (x * data.loc[x.index, 'quantity']).sum() / data.loc[x.index, 'quantity'].sum(),
            # Weighted average entry price
            'exit_price': lambda x: (x * data.loc[x.index, 'quantity']).sum() / data.loc[x.index, 'quantity'].sum(),
            # Weighted average exit price
            'quantity': 'sum',  # Sum up the quantities
            'profit': 'sum',  # Sum up the profit
            'com': 'sum'  # Sum up the commissions
        }
    ).reset_index()

    return grouped_data
