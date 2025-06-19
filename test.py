import sys
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

class BarRectItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, rect, profit, trade_info, positiveBrush, negativeBrush, hoverBrush, parent=None):
        super().__init__(rect, parent)
        self.profit = profit
        self.trade_info = trade_info
        self.positiveBrush = QtGui.QBrush(QtGui.QColor(positiveBrush))
        self.negativeBrush = QtGui.QBrush(QtGui.QColor(negativeBrush))
        self.hoverBrush = QtGui.QBrush(QtGui.QColor(hoverBrush))
        # Set the initial color based on profit sign.
        if profit >= 0:
            self.setBrush(self.positiveBrush)
        else:
            self.setBrush(self.negativeBrush)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        # Change the brush on hover and show tooltip.
        self.setBrush(self.hoverBrush)
        QtWidgets.QToolTip.showText(event.screenPos(), self.trade_info)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Restore original color and hide tooltip.
        if self.profit >= 0:
            self.setBrush(self.positiveBrush)
        else:
            self.setBrush(self.negativeBrush)
        QtWidgets.QToolTip.hideText()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        print(f"Bar clicked! Profit: {self.profit}")
        super().mousePressEvent(event)

class BarGraphWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create a QGraphicsView and QGraphicsScene.
        self.view = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view.setScene(self.scene)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        # Style the view (background color, etc.)
        self.view.setStyleSheet("background-color: #333333;")
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)

    def update_graph(self, data):
        # Clear previous items.
        try:
            self.scene.clear()

            # Process data: convert columns to appropriate types.
            data['entry_time'] = pd.to_datetime(data['entry_time'], errors='coerce')
            data['profit'] = pd.to_numeric(data['profit'], errors='coerce')
            data = data.dropna(subset=['entry_time', 'profit'])
            # Group data so that each row represents one trade.
            grouped = data.groupby('entry_time').agg(
                profit=('profit', 'sum'),
                direction=('direction', 'first'),
                instrument=('instrument', 'first'),
                exit_time=('exit_time', 'last'),
                trade_id=('trade_id', 'first')
            ).reset_index()

            n = len(grouped)
            bar_width = 20
            spacing = 5
        except Exception as e:
            print(f'PART 1: {e}')
            return
        try:
            # Set a simple scale: profit value maps directly to pixel height.
            # You may want to adjust the scale for your data.
            for i, row in grouped.iterrows():
                profit = row['profit']
                x = i * (bar_width + spacing)
                # If profit is negative, we want the bar to extend downward.
                if profit >= 0:
                    rect = QtCore.QRectF(x, -profit, bar_width, profit)
                else:
                    rect = QtCore.QRectF(x, 0, bar_width, -profit)
                trade_info = (f"Trade {i+1}\n"
                              f"Profit: {profit:.2f}\n"
                              f"Direction: {row['direction']}\n"
                              f"Instrument: {row['instrument']}\n"
                              f"Entry Time: {row['entry_time']}\n"
                              f"Exit Time: {row['exit_time']}\n"
                              f"Trade ID: {row['trade_id']}")
                # Create a BarRectItem for each trade.
                bar_item = BarRectItem(rect, profit, trade_info,
                                       positiveBrush="green",
                                       negativeBrush="red",
                                       hoverBrush="yellow")
        except Exception as e:
            print(f'PART 2: {e}')
        try:
        self.scene.addItem(bar_item)
        # Draw a horizontal line at y = 0.
        line = self.scene.addLine(0, 0, n * (bar_width + spacing), 0, QtGui.QPen(QtGui.QColor("white"), 2))
        # Adjust the scene's bounding rectangle.
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = BarGraphWidget()
    # Create dummy data.
    data = pd.DataFrame({
        'entry_time': pd.date_range('2021-01-01', periods=10, freq='D'),
        'profit': np.random.randint(-150, 200, 10),
        'direction': np.random.choice(['buy', 'sell'], 10),
        'instrument': np.random.choice(['AAPL', 'GOOG', 'MSFT'], 10),
        'exit_time': pd.date_range('2021-01-02', periods=10, freq='D'),
        'trade_id': range(1, 11)
    })
    widget.update_graph(data)
    widget.setWindowTitle("Bar Graph Using QGraphicsRectItem")
    widget.resize(600, 400)
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
