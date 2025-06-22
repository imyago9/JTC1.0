import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mplcursors

class BarGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.figure = Figure(facecolor='#333333')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.ax = self.figure.add_subplot(111)
        self._initialize_chart_style()

    def _initialize_chart_style(self):
        self.ax.set_title("P&L Bar Chart", color='white')
        self.ax.set_facecolor('#333333')
        self.figure.patch.set_facecolor('#333333')
        for spine in self.ax.spines.values():
            spine.set_color('#c3dc9b')
        self.ax.tick_params(axis='x', colors='white', rotation=45)
        self.ax.tick_params(axis='y', colors='white')
        self.ax.grid(False)

    def update_graph(self, data):
        try:
            data = pd.DataFrame(data)
            data['entry_time'] = pd.to_datetime(data['entry_time'], errors='coerce')
            data['profit'] = pd.to_numeric(data['profit'], errors='coerce')
            data = data.dropna(subset=['entry_time', 'profit'])

            grouped = data.groupby('entry_time').agg(
                profit=('profit', 'sum'),
                direction=('direction', 'first'),
                instrument=('instrument', 'first'),
                exit_time=('exit_time', 'last'),
                trade_id=('trade_id', 'first'),
            ).reset_index()

            x_positions = np.arange(len(grouped))
            profits = grouped['profit'].values

            self.ax.clear()
            self._initialize_chart_style()

            bars = self.ax.bar(x_positions, profits, color='blue', width=0.6)
            self.ax.set_xticks(x_positions)
            self.ax.set_xticklabels(grouped['entry_time'].dt.strftime('%Y-%m-%d %H:%M:%S'))

            mplcursors.cursor(bars, hover=True).connect(
                "add", lambda sel: sel.annotation.set_text(
                    f"Entry Time: {grouped.iloc[sel.index]['entry_time']}\n"
                    f"Profit: {grouped.iloc[sel.index]['profit']}\n"
                    f"Direction: {grouped.iloc[sel.index]['direction']}\n"
                    f"Instrument: {grouped.iloc[sel.index]['instrument']}\n"
                    f"Exit Time: {grouped.iloc[sel.index]['exit_time']}\n"
                    f"Trade ID: {grouped.iloc[sel.index]['trade_id']}"
                )
            )
            self.canvas.draw()
        except Exception as e:
            print(f"Error updating bar graph: {e}")
