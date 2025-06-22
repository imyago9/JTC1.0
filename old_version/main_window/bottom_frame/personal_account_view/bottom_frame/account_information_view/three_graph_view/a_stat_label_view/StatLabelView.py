from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QFrame


class StatLabelView(QFrame):
    def __init__(self, parent=None, icons=None, money_visible=True):
        super().__init__(parent)
        self.icons = icons or {}
        self.money_visible = money_visible

        self.first_stats_label = QLabel()
        self.second_stats_label = QLabel()
        self.third_stats_label = QLabel()

        self.money_visibility_button = QPushButton()
        self.add_new_trade_button = QPushButton()

        self.correct_label = ''

        self.layout = QHBoxLayout(self)
        self.setupUI()

    def setupUI(self):
        # First stats frame
        first_stats_frame = QFrame()
        first_stats_layout = QHBoxLayout(first_stats_frame)

        first_stats_layout.addWidget(self.money_visibility_button, alignment=Qt.AlignLeft)
        first_stats_layout.addWidget(self.first_stats_label)

        # Second stats frame
        second_stats_frame = QFrame()
        second_stats_layout = QHBoxLayout(second_stats_frame)

        self.second_stats_label.setText('Information will be displayed here.')
        self.second_stats_label.setAlignment(Qt.AlignCenter)

        second_stats_layout.addWidget(self.second_stats_label)

        # Third stats frame
        third_stats_frame = QFrame()
        third_stats_layout = QHBoxLayout(third_stats_frame)

        self.add_new_trade_button.setIcon(self.icons.get("add_trade", QIcon()))
        self.money_visibility_button.setIcon(self.icons.get("view", QIcon()))

        third_stats_layout.addWidget(self.third_stats_label)
        third_stats_layout.addWidget(self.add_new_trade_button, alignment=Qt.AlignRight)

        # Add to main layout
        self.layout.addWidget(first_stats_frame)
        self.layout.addWidget(second_stats_frame)
        self.layout.addWidget(third_stats_frame)

    def updateLabels(self, stats):
        try:
            # Update labels with stats
            if stats:
                avg_win = f'{stats["avg_win"]:.2f}' if self.money_visible else '---'
                avg_loss = f'{stats["avg_loss"]:.2f}' if self.money_visible else '---'
                net_pnl = f'{stats["net_pnl"]:.2f}' if self.money_visible else '---'
                if net_pnl != '---':
                    np_color = '#c3dc9b' if float(net_pnl) > 0 else '#ff7f7f'
                else:
                    np_color = 'white'

                self.first_stats_label.setText(f'<span style="color:#c3dc9b;">Avg Win: </span>'
                                               f'<span style="color:white;">${avg_win}</span><br>'
                                               f'<span style="color:#ff7f7f;">Avg Loss: </span>'
                                               f'<span style="color:white;">${avg_loss}</span><br>'
                                               f'<span style="color:#f4e66e;">Avg RR ratio: </span>'
                                               f'<span style="color:white;">{stats["avg_rr"]:.2f}</span>')
                self.second_stats_label.setText(f'<span style="color:white;">Number of Trades: </span>'
                                                f'<span style="color:#c3dc9b;"> {stats['total_trades']}</span><br>'
                                                f'<span style="color:white;">Net Profit: </span>'
                                                f'<span style="color:{np_color};"> {net_pnl} </span>')
                self.correct_label = self.second_stats_label.text()
                self.third_stats_label.setText(f'<span style="color:#c3dc9b;">Win Rate: </span>'
                                               f'<span style="color:white;">{stats["win_rate"]:.2f}%</span><br>'
                                               f'<span style="color:#ff7f7f;">Loss Rate: </span>'
                                               f'<span style="color:white;">{stats["loss_rate"]:.2f}%</span><br>'
                                               f'<span style="color:#f4e66e;">B/e Rate: </span>'
                                               f'<span style="color:white;">{stats["break_even_rate"]:.2f}%</span>')
            else:
                print('NAHHHH')
        except Exception as e:
            print(f'Error updating stats labels: {e}')