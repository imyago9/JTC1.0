import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class LineGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Create a Matplotlib figure and canvas
        self.figure = Figure(facecolor='#333333')  # Similar to fig.patch in Matplotlib
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        # Create an axes for plotting
        self.ax = self.figure.add_subplot(111)
        self._initialize_chart_style()

    def _initialize_chart_style(self):
        # Set the background color for the axes
        self.ax.set_facecolor('#333333')
        # Set the title with white text
        self.ax.set_title('P&L Chart', color='white')

        # Style the spines: set their color to a custom color
        for spine in self.ax.spines.values():
            spine.set_color('#c3dc9b')

        # Set tick label colors for both axes
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        # Disable grid lines
        self.ax.grid(False)

    def update_graph(self, data):
        try:
            # Convert input to DataFrame
            data = pd.DataFrame(data)
            if not isinstance(data, pd.DataFrame):
                print("Error: Expected a Pandas DataFrame")
                return

            # Ensure 'entry_time' is datetime and 'profit' is numeric
            data['entry_time'] = pd.to_datetime(data['entry_time'], errors='coerce')
            data['profit'] = pd.to_numeric(data['profit'], errors='coerce')

            # Drop rows with NaN values in 'entry_time' or 'profit'
            data = data.dropna(subset=['entry_time', 'profit'])

            # Compute the cumulative sum of profit grouped by entry_time
            grouped = data.groupby('entry_time')['profit'].sum().cumsum()

            # Clear the axes and reapply styling
            self.ax.clear()
            self._initialize_chart_style()

            # Plot the cumulative progress as a green line with a linewidth of 5
            self.ax.plot(grouped.index, grouped.values, color='green', linewidth=5)

            # Optionally, format the x-axis to display dates nicely
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            self.figure.autofmt_xdate()

            # Redraw the canvas to update the graph
            self.canvas.draw()
        except Exception as e:
            print(f'Error updating line graph: {e}')
