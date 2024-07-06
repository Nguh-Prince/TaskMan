from PyQt5.QtCore import QObject, Qt, QEvent
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QTableWidget

class Table(QTableWidget):
    def __init__(
            self, numberOfRows, numberOfColumns, 
            horizontalHeaderLabels=[], showGrid=False, showVerticalHeader=False
        ):
        super().__init__()
        self.setRowCount(numberOfRows)
        self.setColumnCount(numberOfColumns)
        self.setShowGrid(showGrid)

        self.setHorizontalHeaderLabels(horizontalHeaderLabels)
        self.verticalHeader().setVisible(showVerticalHeader)

        self.viewport().installEventFilter(self)

        self.last_row = -1

    def eventFilter(self, source, event):
        

        return super().eventFilter(source, event)

    # def setHoverBackground(self, row):
    #     for column in range(self.columnCount()):
    #         item = self.item(row, column)

    #         if item:
    #             item.setBackground(QBrush(QColor("#f6f6f6")))
    #     pass

    # def clearHoverBackground(self, row):
    #     if row >= 0:
    #         for column in range(self.columnCount()):
    #             item = self.item(row, column)
    #             if item:
    #                 item.setBackground(QBrush(Qt.white))