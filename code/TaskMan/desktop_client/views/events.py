from PyQt5.QtCore import QObject, Qt, QEvent
from PyQt5.QtGui import QColor, QBrush

class HoverEventFilter(QObject):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.last_row = -1  # Track the last hovered row

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter:
            print("Hovered over a process")
            index = self.table.indexAt(event.pos())
            if index.isValid():
                current_row = index.row()
                if current_row != self.last_row:
                    self.clear_hover_background(self.last_row)
                    self.set_hover_background(current_row)
                    self.last_row = current_row
        elif event.type() == QEvent.Leave:
            self.clear_hover_background(self.last_row)
            self.last_row = -1
        return super().eventFilter(source, event)

    def set_hover_background(self, row):
        for column in range(self.table.columnCount()):
            item = self.table.item(row, column)
            if item:
                item.setBackground(QBrush(QColor("#D3D3D3")))  # Light gray color

    def clear_hover_background(self, row):
        if row >= 0:
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item:
                    item.setBackground(QBrush(Qt.white))
