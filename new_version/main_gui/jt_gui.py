from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

from custom_widgets.custom_widgets import CustomFrameWindow


class JournalTradeGUI(CustomFrameWindow):
    logout_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JournalTrade')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.home_label = QLabel("Welcome to JournalTrade")
        self.home_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.home_label)
        btn = QPushButton("Log out")
        btn.clicked.connect(self.logout_requested.emit)
        self.layout.addWidget(btn)