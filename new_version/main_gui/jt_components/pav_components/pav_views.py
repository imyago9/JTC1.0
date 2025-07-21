from enum import Enum, auto
import pyqtgraph as pg
from pyqtgraph import PlotWidget, PlotDataItem
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout,
    QFrame, QDateEdit, QSizePolicy, QStackedWidget,
    QGraphicsOpacityEffect, QLineEdit, QScrollArea)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from utils import ResourceLoader, vbox, grid, hbox

class AccountCreationView(QWidget):
    pressed_back = pyqtSignal()
    pressed_create_account = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        lay = vbox(self)
        lbl1 = QLabel("Create New Account", objectName="ACV_label1", alignment=Qt.AlignHCenter) # type: ignore
        lbl2 = QLabel("Choose a name for your account!", objectName="ACV_label2", alignment=Qt.AlignHCenter) # type: ignore
        b_create_account = QPushButton("Create Account", objectName="ACV_create_account", cursor=Qt.PointingHandCursor, clicked=lambda: self.pressed_create_account.emit(self.account_name.text())) # type: ignore
        self.account_name = QLineEdit(placeholderText='Enter account name', objectName="ACV_account_name", alignment=Qt.AlignHCenter) # type: ignore
        b_back = QPushButton("Back", objectName="ACV_button_back", clicked=self._back_reset_text, cursor=Qt.PointingHandCursor) # type: ignore

        lay.addWidget(lbl1)
        lay.addWidget(lbl2)
        lay.addStretch(1)
        lay.addWidget(self.account_name)
        lay.addStretch(1)
        lay.addWidget(b_create_account)
        lay.addWidget(b_back)

    def _back_reset_text(self):
        self.account_name.setText('')
        self.pressed_back.emit() # type: ignore


class AccountCard(QFrame):
    def __init__(self, account_obj, parent=None):
        super().__init__(parent)
        self.account_data = account_obj
        self.setObjectName("ASV_card")
        self.setCursor(Qt.PointingHandCursor)
        # --- layout
        hl = hbox(self)
        name = account_obj if isinstance(account_obj, str) else account_obj.get("name", "")
        lbl = QLabel(name, self)
        hl.addWidget(lbl)

    # expose a clicked signal like a button
    clicked = pyqtSignal(object)
    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit(self.account_data)
        super().mouseReleaseEvent(ev)

class AccountSelectionView(QWidget):
    pressed_back = pyqtSignal()
    pressed_account_selected = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('ASV_account_selection_view')
        self._build_ui()

    def load_accounts(self, accounts):
        while self._card_layout.count():
            item = self._card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for acc in accounts:
            card = AccountCard(acc)
            card.clicked.connect(self.pressed_account_selected)
            self._card_layout.addWidget(card)

    def _build_ui(self):
        lay = vbox(self, margin=6, spacing=24)
        lbl1 = QLabel("Select an Account", objectName="ASV_label1", alignment=Qt.AlignHCenter) # type: ignore , alignment=Qt.AlignCenter
        b_back = QPushButton("Back", objectName="ASV_button_back", clicked=self.pressed_back, cursor=Qt.PointingHandCursor) # type: ignore

        self._scroll = QScrollArea(objectName="ASV_scroll_area") # type: ignore
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        container = QWidget()
        self._card_layout = vbox(container, margin=12, spacing=6)
        self._scroll.setWidget(container)

        lay.addWidget(lbl1)
        # lay.addStretch(1)
        lay.addWidget(self._scroll)
        # lay.addStretch(1)
        lay.addWidget(b_back)

        self.load_accounts(["Personal Check2ing", "Sav3ings", "Cryp3to Wallet","Personal Checki25ng","Personal Check2ing", "Sav3i1ngs", "Cryp3t4o Wallet","Perso234nal Checki25ng","Perso234nal Chec34k2ing", "Sa134v3ings1", "Cryp334to Wallet","Personal Checki25ng"])

class LineGraphView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot = PlotWidget(background="#121212")   # dark mode
        self.curve: PlotDataItem = self.plot.plot(pen={'color': '#8DEB7A', 'width': 2})
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        lay = vbox(self)
        lay.addWidget(self.plot)


    def set_data(self, data):
        """Set graph data from a list of {'date', 'profit'} dictionaries."""
        import numpy as np
        dates = [d["date"] for d in data]
        profits = [d["profit"] for d in data]
        x = np.arange(len(dates))
        self.curve.setData(x, profits)
        # show day numbers on the x axis
        ticks = [(i, str(date.day)) for i, date in enumerate(dates)]
        self.plot.getPlotItem().getAxis("bottom").setTicks([ticks])
        self.plot.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

class BarGraphView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot = PlotWidget(background="#121212")
        self.bar = None
        lay = vbox(self); lay.addWidget(self.plot)

    def set_data(self, data):
        """Set bar graph data from a list of {'date', 'profit'} dictionaries."""
        import numpy as np

        dates = [d["date"] for d in data]
        profits = [d["profit"] for d in data]
        x = np.arange(len(dates))
        if self.bar is not None:
            self.plot.removeItem(self.bar)
        self.bar = pg.BarGraphItem(x=x, height=profits, width=0.8,
                                   brush=pg.mkBrush("#65C1FF"))
        self.plot.addItem(self.bar)
        self.plot.enableAutoRange()
        ticks = [(i, str(date.day)) for i, date in enumerate(dates)]
        self.plot.getPlotItem().getAxis("bottom").setTicks([ticks])
        self.plot.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

class CalendarView(QWidget):
    date_range_changed = pyqtSignal(QDate, QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._data = []

    def _build_ui(self):
        layout = vbox(self)
        page = QWidget()
        outer = vbox(page)

        date_row = QHBoxLayout()
        self.start_edit = QDateEdit(QDate.currentDate(), objectName="PAV_dateedit_start", calendarPopup=True) # type: ignore
        self.end_edit = QDateEdit(QDate.currentDate(), objectName="PAV_dateedit_end", calendarPopup=True) # type: ignore
        self.start_edit.dateChanged.connect(self._on_date_changed)
        self.end_edit.dateChanged.connect(self._on_date_changed)

        date_row.addWidget(self.start_edit)
        date_row.addWidget(self.end_edit)
        outer.addLayout(date_row)

        # calendar grid
        cal = grid()
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            cal.addWidget(QLabel(d, objectName=f"PAV_calendar_day_{d}"), 0, i)

        self.cells = []
        for r in range(1, 7):
            row_cells = []
            for c in range(7):
                cell = QLabel("", objectName=f"PAV_calendar_cell_{r}_{c}")
                cell.setFrameShape(QFrame.Box)
                cell.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                cal.addWidget(cell, r, c)
                row_cells.append(cell)
            self.cells.append(row_cells)

        outer.addLayout(cal)
        layout.addWidget(page)

    def set_data(self, data):
        """Display profit data on the calendar grid."""
        import calendar

        self._data = data
        if not data:
            return

        start_date = data[0]["date"]
        year, month = start_date.year, start_date.month

        profits = {d["date"].day: d["profit"] for d in data
                   if d["date"].month == month and d["date"].year == year}

        month_matrix = calendar.monthcalendar(year, month)
        for r in range(6):
            week = month_matrix[r] if r < len(month_matrix) else [0]*7
            for c, day in enumerate(week):
                label = self.cells[r][c]
                if day == 0:
                    label.setText("")
                else:
                    profit = profits.get(day, "")
                    text = f"{day}\n{profit}" if profit != "" else str(day)
                    label.setText(text)
                    label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)


    def _on_date_changed(self, *_):
        self.date_range_changed.emit(self.start_edit.date(),
                                     self.end_edit.date())
