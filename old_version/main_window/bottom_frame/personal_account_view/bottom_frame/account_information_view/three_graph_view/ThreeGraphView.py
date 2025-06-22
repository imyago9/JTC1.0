import pandas as pd

from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QLabel, QHBoxLayout, QFrame, QVBoxLayout

from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.ThreeGraphViewModel import \
    ThreeGraphViewModel
from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.a_stat_label_view.StatLabelView import \
    StatLabelView
from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.bar_graph_view.BarGraphView import \
    BarGraphWidget
from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.calendar_graph_view.CalendarGraphView import \
    CalendarGraphWidget
from old_version.main_window.bottom_frame.personal_account_view.bottom_frame.account_information_view.three_graph_view.line_graph_view.LineGraphView import \
    LineGraphWidget


class ViewState(Enum):
    EMPTY_VIEW = 'empty_view'
    FILLED_VIEW = 'filled_view'
    DAILY_NOTE_VIEW = 'daily_note_view'


class ThreeGraphView(QFrame):
    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.view_model = ThreeGraphViewModel()
            self.layout = QVBoxLayout(self)

            self.stats_label_view = StatLabelView(self, icons=self.parent().parent().icons)
            self.stats_label_view.add_new_trade_button.clicked.connect(self.parent().new_trade_button_pressed)
            # self.stats_frame.money_visibility_button.clicked.connect(self.graphs_manager.visibilityButtonPressed)

            self.stacks_layout = QHBoxLayout(self)
            self.first_stack_view = QStackedWidget(self)
            self.second_stack_view = QStackedWidget(self)
            self.third_stack_view = QStackedWidget(self)

            self.line_graph = LineGraphWidget(parent=self.first_stack_view)
            self.bar_graph = BarGraphWidget(parent=self.second_stack_view)
            self.calendar_graph = CalendarGraphWidget(parent=self.third_stack_view)

            self.first_stack_view.addWidget(self.line_graph)
            self.second_stack_view.addWidget(self.bar_graph)
            self.third_stack_view.addWidget(self.calendar_graph)

            for stack in [self.first_stack_view, self.second_stack_view, self.third_stack_view]:
                self.stacks_layout.addWidget(stack, 1)
                stack.setAttribute(Qt.WA_DeleteOnClose, False)

            label1 = QLabel("")

            label2 = QLabel("Graphs will display here!")
            label2.setStyleSheet("color: white; font-style: italic;")
            label2.setAlignment(Qt.AlignCenter)

            label3 = QLabel("")

            self.first_stack_view.addWidget(label1)
            self.first_stack_view.setCurrentWidget(label1)

            self.second_stack_view.addWidget(label2)
            self.second_stack_view.setCurrentWidget(label2)

            self.third_stack_view.addWidget(label3)
            self.third_stack_view.setCurrentWidget(label3)

            self.parent().AIV_updates_TGV.connect(self.update_graphs)

            self.layout.addWidget(self.stats_label_view)
            self.layout.addLayout(self.stacks_layout)
        except Exception as e:
            print(f'Error initializing three graph view: {e}')

    def set_stats_label_text(self, text1, text2, text3):
        try:
            self.stats_label_view.first_stats_label.setText(text1)
            self.stats_label_view.second_stats_label.setText(text2)
            self.stats_label_view.third_stats_label.setText(text3)
        except Exception as e:
            print(f'Error setting stats label text: {e}')

    def update_graphs(self):
        """Updates all three graphs when new trade data is received."""
        try:
            stats = self.view_model.get_stats_data()
            trade_data = self.view_model.get_trade_data()
            if stats and trade_data:
                self.stats_label_view.updateLabels(stats)
                self.update_line_graph(trade_data)
                self.update_bar_graph(trade_data)
                self.update_calendar_graph(trade_data)
        except Exception as e:
            print(f'Error updating graphs: {e}')

    def update_line_graph(self, trade_data):
        """Safely update the line graph to prevent deletion issues."""
        try:
            if self.line_graph:
                if self.first_stack_view.currentWidget() != self.line_graph:
                    self.first_stack_view.setCurrentWidget(self.line_graph)
                self.line_graph.update_graph(trade_data)  # Calls the print function
        except Exception as e:
            print(f'Error updating line graph: {e}')

    def update_bar_graph(self, trade_data):
        """Safely update the bar graph to prevent deletion issues."""
        try:
            if self.bar_graph:
                if self.second_stack_view.currentWidget() != self.bar_graph:
                    self.second_stack_view.setCurrentWidget(self.bar_graph)
                self.bar_graph.update_graph(trade_data)  # Calls the print function
        except Exception as e:
            print(f'Error updating bar graph: {e}')

    def update_calendar_graph(self, trade_data):
        """Safely update the calendar graph to prevent deletion issues."""
        try:
            if self.calendar_graph:
                if self.third_stack_view.currentWidget() != self.calendar_graph:
                    self.third_stack_view.setCurrentWidget(self.calendar_graph)
                self.calendar_graph.update_graph(trade_data)  # Calls the print function
        except Exception as e:
            print(f'Error updating calendar graph: {e}')