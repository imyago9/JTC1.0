from enum import Enum, auto
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QFrame, QStackedWidget,
    QGraphicsOpacityEffect)
from PyQt5.QtCore import Qt, QDate
from main_gui.jt_components.pav_components.pav_views import (LineGraphView, AccountCreationView,
                                                             AccountSelectionView, BarGraphView,
                                                             CalendarView)
from utils import ResourceLoader, translucent_label, vbox, grid, hbox, change_opacity, mock_data

class CenterPages(Enum):
    HOME = auto()
    CREATE_ACCOUNT = auto()
    SELECT_ACCOUNT = auto()
    ACCOUNT_VIEW = auto()

class PersonalAccountsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._center_pages = {}
        self.main_layout = vbox(self)
        self.setLayout(self.main_layout)

        self._selected_account = None
        self._build_ui()
        self._set_current_page(CenterPages.HOME)

    def _build_ui(self):
        self._setup_top_header()
        self._setup_statistic_boxes()
        self._setup_main_area()

    # ────────────────────────── Top  ─────────────────────────────
    def _setup_top_header(self): # This is invisible at first and only shows when an account is selected.
        hdr = vbox()
        self.account_status_lbl = QLabel("", objectName="PAV_account_status", alignment=Qt.AlignHCenter | Qt.AlignVCenter) # type: ignore
        self.b_h_account_select = QPushButton("Return Home", objectName="PAV_select_account", clicked=lambda: self._set_current_page(CenterPages.HOME), cursor=Qt.PointingHandCursor, visible=False) # type: ignore
        hdr.addWidget(self.account_status_lbl)
        hdr.addWidget(self.b_h_account_select, alignment=Qt.AlignHCenter | Qt.AlignVCenter) # type: ignore
        w = int(self.width()*0.4)  # Set a maximum width for the button
        self.b_h_account_select.setMaximumWidth(w)
        self.main_layout.addLayout(hdr)
    # ────────────────────────── Middle ─────────────────────────────
    def _setup_statistic_boxes(self):
        row = hbox(margin=24, spacing=12)
        for i in range(3):
            box = QLabel("", objectName=f"PAV_stat_box_{i}")
            box.setFrameShape(QFrame.Box)
            row.addWidget(box)
        self.main_layout.addLayout(row)
    # ────────────────────────── Bottom ─────────────────────────────
    def _setup_main_area(self):
        # ╭─ Setting up grid  ───────────────────────────────────────╮
        grid_layout = grid(margin=24, spacing=12)
        for col in range(3):
            grid_layout.setColumnStretch(col, 1)
        # ╭─ Setting up stacks  ─────────────────────────────────────╮
        self.left_stack   = QStackedWidget(objectName="PAV_left_stack")
        self.center_stack = QStackedWidget(objectName="PAV_center_stack")
        self.right_stack  = QStackedWidget(objectName="PAV_right_stack")
        # ╭─ Building Pages  ─────────────────────────────────────╮
        self._build_left_page()
        self._build_center_pages()
        self._build_right_page()
        # ╭─ Adding stacks to the grid layout + to the main layout ───╮
        grid_layout.addWidget(self.left_stack,   0, 0)
        grid_layout.addWidget(self.center_stack, 0, 1)
        grid_layout.addWidget(self.right_stack,  0, 2)
        self.main_layout.addLayout(grid_layout)

    # ────────────────────────── Bottom Left  ─────────────────────────────
    def _build_left_page(self):
        # ╭─ Home Filler  ─────────────────────────────────────────────╮
        self.left_page = QWidget()
        lay = vbox(self.left_page)
        pix = ResourceLoader.get_background("line_graph")
        img = translucent_label(pix, 'PAV_line_graph')
        lay.addWidget(img)
        # ╭─ Interactive Widget  ──────────────────────────────────────╮
        self.line_graph_view = LineGraphView()
        # ╭─ Adding into left stack  ──────────────────────────────────╮
        self.left_stack.addWidget(self.left_page)
        self.left_stack.addWidget(self.line_graph_view)

    # ────────────────────────── Bottom Center  ─────────────────────────────
    def _build_center_pages(self):
        # ╭─ Home Filler  ──────────────────────────────────────────────╮
        self._center_pages[CenterPages.HOME] = self._center_home_page()
        # ╭─ Account Creation View  ────────────────────────────────────╮
        acv = AccountCreationView()
        acv.pressed_back.connect(lambda: self._set_current_page(CenterPages.HOME))
        acv.pressed_create_account.connect(self._account_created)
        self._center_pages[CenterPages.CREATE_ACCOUNT] = acv
        # ╭─ Account Selection View ────────────────────────────────────╮
        asv = AccountSelectionView()
        asv.pressed_back.connect(lambda: self._set_current_page(CenterPages.HOME))
        asv.pressed_account_selected.connect(self._account_selected)
        self._center_pages[CenterPages.SELECT_ACCOUNT] = asv
        # ╭─ Account View ──────────────────────────────────────────────╮
        self.bar_graph_view = BarGraphView()
        # ╭─ Adding into center stack ──────────────────────────────────╮
        for center_page in self._center_pages.values():
            self.center_stack.addWidget(center_page)
        self.center_stack.addWidget(self.bar_graph_view)
    def _center_home_page(self):
        # ╭─ Center Home Filler + Account Actions ───────────────────────────────────────╮
        home_page = QWidget()
        lay  = vbox(home_page)
        lbl1 = QLabel("No Account Selected",     objectName="PAV_label_main_message", alignment=Qt.AlignHCenter) # type: ignore
        lbl2 = QLabel("Choose an account or create one below!", # type: ignore
                      objectName="PAV_label_sub_message", alignment=Qt.AlignHCenter) # type: ignore , alignment=Qt.AlignCenter
        pix = ResourceLoader.get_background("bar_graph")
        img = translucent_label(pix, 'PAV_bar_graph')
        b_select_account  = QPushButton("Select Account", objectName="PAV_select_account", clicked=lambda: self._set_current_page(CenterPages.SELECT_ACCOUNT), cursor=Qt.PointingHandCursor) # type: ignore
        b_add_account  = QPushButton("Add Account", objectName="PAV_add_account", clicked=lambda: self._set_current_page(CenterPages.CREATE_ACCOUNT), cursor=Qt.PointingHandCursor) # type: ignore
        lay.addWidget(lbl1); lay.addWidget(lbl2); lay.addStretch(); lay.addWidget(img); lay.addStretch(); lay.addWidget(b_select_account); lay.addWidget(b_add_account)
        return home_page

    # ────────────────────────── Bottom Right  ─────────────────────────────
    def _build_right_page(self):
        # ╭─ Home Filler  ──────────────────────────────────────────────╮
        self.right_page = QWidget()
        lay = vbox(self.right_page)
        pix = ResourceLoader.get_background("calendar")
        img = translucent_label(pix, 'PAV_calendar')
        lay.addWidget(img)
        self.right_stack.addWidget(self.right_page)
        # ╭─ Interactive Widgets ───────────────────────────────────────╮
        self.calendar_view = CalendarView()
        self.calendar_view.date_range_changed.connect(self._refresh_charts)
        self.right_stack.addWidget(self.calendar_view)

    # ────────────────────────── Helper Functions  ─────────────────────────────
    def _set_current_page(self, page: CenterPages):
        change_opacity((self.left_stack, self.right_stack),
                       1 if page in (CenterPages.HOME, CenterPages.ACCOUNT_VIEW) else 0)
        if page == CenterPages.ACCOUNT_VIEW:
            self.b_h_account_select.setVisible(True)
            self.left_stack.setCurrentWidget(self.line_graph_view)
            self.center_stack.setCurrentWidget(self.bar_graph_view)
            self.right_stack.setCurrentWidget(self.calendar_view)
            return
        if page == CenterPages.HOME:
            self.account_status_lbl.setText('')
            self.left_stack.setCurrentWidget(self.left_page)
            self.right_stack.setCurrentWidget(self.right_page)
        self.b_h_account_select.setVisible(False)
        self.center_stack.setCurrentWidget(self._center_pages[page])
    def _account_created(self, data):
        print(f"Account created with name: {data}")
        self._set_current_page(CenterPages.SELECT_ACCOUNT)
    def _account_selected(self, account_name):
        self._selected_account = account_name
        self.account_status_lbl.setText(account_name)
        self._set_current_page(CenterPages.ACCOUNT_VIEW)
        self._refresh_charts()
        print(f"Account selected: {account_name}")
    def _refresh_charts(self, start: QDate = None, end: QDate = None):
        if self._selected_account is None:
            return
        start = start or self.calendar_view.start_edit.date()
        end = end or self.calendar_view.end_edit.date()
        data = mock_data(start, end)
        self.line_graph_view.set_data(data)
        self.bar_graph_view.set_data(data)
        self.calendar_view.set_data(data)