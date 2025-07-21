import sys

from PyQt5.QtGui import QPainterPath, QRegion, QBrush, QPalette
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QSize

from custom_widgets.custom_widgets import CustomFrameWindow
from main_gui.jt_components.personal_accounts_view import PersonalAccountsView
from utils import ResourceLoader, grid, hbox


class JournalTradeGUI(CustomFrameWindow):
    logout_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JournalTrade')

        self.RADIUS = 9
        self._bg_orig = ResourceLoader.get_background("jt_landscape")
        self._is_maximized = False
        self._normal_geometry = None
        self._drag_offset = None
        self._build_ui()

    # ────────────────────────── UI BUILDER ─────────────────────────────
    def _build_ui(self):
        self._build_title_bar()
        self.layout.addWidget(PersonalAccountsView())

    # >────── title bar ──────────────────────────────────────────────────<
    def _build_title_bar(self):
        # ╭─ Left section  ──────────────────────────────────────────────╮
        b_logout = QPushButton(clicked=self.logout_requested.emit, objectName='JTG_logout', toolTip='Logout', icon=ResourceLoader.get_icon("logout"), cursor=Qt.PointingHandCursor) # type: ignore
        b_logout.setIconSize(QSize(24, 24))
        left_container = QWidget()
        left_layout = hbox(left_container)
        left_layout.addWidget(b_logout)
        left_layout.addStretch()
        # ╭─ Center Logo  ───────────────────────────────────────────────╮
        logo_label = QLabel(objectName='logo_label', alignment=Qt.AlignHCenter, pixmap = ResourceLoader.get_icon("jt_logo").pixmap(ResourceLoader.get_icon("jt_logo").availableSizes()[0])) # type: ignore
        # ╭─ right section (window controls) ────────────────────────────╮
        self.b_max_restore = QPushButton(clicked=self._toggle_max_restore, objectName='JTG_maximize', toolTip='Maximize app.', icon=ResourceLoader.get_icon("expand_icon"), cursor=Qt.PointingHandCursor) # type: ignore
        b_minimize = QPushButton(clicked=self.showMinimized, objectName='JTG_minimize', toolTip='Hide app.', icon=ResourceLoader.get_icon('minimize_window'), cursor=Qt.PointingHandCursor) # type: ignore
        b_close = QPushButton(clicked=sys.exit, objectName='JTG_close', toolTip='Exit app.', icon=ResourceLoader.get_icon("close_window"), cursor=Qt.PointingHandCursor) # type: ignore
        right_container = QWidget()
        right_layout = hbox(right_container)
        right_layout.addStretch()
        right_layout.addWidget(self.b_max_restore)
        right_layout.addWidget(b_minimize)
        right_layout.addWidget(b_close)
        # ╭─ tying together ─────────────────────────────────────────────╮
        grid_layout = grid(margin=24)
        grid_layout.addWidget(left_container, 0,0) # type: ignore , alignment=Qt.AlignLeft
        grid_layout.addWidget(logo_label, 0,1) # type: ignore , alignment=Qt.AlignCenter
        grid_layout.addWidget(right_container, 0,2) # type: ignore , alignment=Qt.AlignRight
        self.layout.addLayout(grid_layout)
        self.enable_title_bar_drag(int(left_container.sizeHint().height()*3), allow_double_click_max=True)

    # ────────────────────────── Background Image ─────────────────────────────
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_round_mask()
        self._apply_background()

    def _apply_round_mask(self):
        path  = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self.RADIUS, self.RADIUS)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def _apply_background(self):
        if self.width() == 0 or self.height() == 0:
            return
        scaled = self._bg_orig.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation) # type: ignore
        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(scaled)) # type: ignore
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    # ──────────────────────── Window behaviours ───────────────────────────
    def _toggle_max_restore(self):
        try:
            if not self._is_maximized:
                # save current size/pos only the first time
                self._normal_geometry = self.geometry()
                self.showMaximized()
                self.b_max_restore.setIcon(ResourceLoader.get_icon('shrink_icon'))
                self.b_max_restore.setToolTip('Shrink window')
                self._is_maximized = True
            else:
                self.showNormal()
                # restore size/pos if we have it
                if self._normal_geometry is not None:
                    self.setGeometry(self._normal_geometry)
                self.b_max_restore.setIcon(ResourceLoader.get_icon('expand_icon'))
                self.b_max_restore.setToolTip('Expand app')
                self._is_maximized = False
        except Exception as e:
            print(f"Error in _toggle_max_restore: {e}")






