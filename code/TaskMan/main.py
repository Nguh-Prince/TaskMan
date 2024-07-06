import os, sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QMainWindow, QHeaderView, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPen

from views.events import HoverEventFilter
from views.widgets import Table

icon_path = os.path.abspath("views/icon.png")

class BorderDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Draw the cell background
        painter.save()
        painter.fillRect(option.rect, option.palette.base())
        
        # Draw the text
        QStyledItemDelegate.paint(self, painter, option, index)

        # Draw the vertical border
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        
        painter.restore()


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TaskMan')
        self.setWindowIcon(QIcon(icon_path))

        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.process_tab = QWidget()
        self.services_tab = QWidget()

        self.tab_widget.addTab(self.process_tab, "Processes")
        self.tab_widget.addTab(self.services_tab, "Services")

        self.colors = {
            "low": "#fff4c4",
            "medium": "#f9eca8",
            "high": "#ffe487"
        }

        self.initProcessTab()
        self.initServicesTab()

        self.show()

    def initProcessTab(self):
        layout = QVBoxLayout()
        table = Table(20, 5, ["Name", "CPU", "Memory", "Disk", "Network"] )

        # Set vertical borders only
        # table.setStyleSheet("QTableWidget::item { border-right: 1px solid #dcdcdc; }")

        # Add dummy data
        for i in range(20):
            table.setItem(i, 0, QTableWidgetItem(f"Process {i+1}"))

            cpu_item = QTableWidgetItem(f"{i * 5}%")
            memory_item = QTableWidgetItem(f"{i * 100} MB")
            disk_item = QTableWidgetItem(f"{i * 10} MB/s")
            network_item = QTableWidgetItem(f"{i * 50} KB/s")

            # Set colors based on usage
            cpu_item.setBackground(QColor(self.colors['high']) if i > 15 else QColor(self.colors['medium']) if i > 10 else QColor(self.colors['low']))
            memory_item.setBackground(QColor(self.colors['high']) if i > 15 else QColor(self.colors['medium']) if i > 10 else QColor(self.colors['low']))
            disk_item.setBackground(QColor(self.colors['high']) if i > 15 else QColor(self.colors['medium']) if i > 10 else QColor(self.colors['low']))
            network_item.setBackground(QColor(self.colors['high']) if i > 15 else QColor(self.colors['medium']) if i > 10 else QColor(self.colors['low']))

            table.setItem(i, 1, cpu_item)
            table.setItem(i, 2, memory_item)
            table.setItem(i, 3, disk_item)
            table.setItem(i, 4, network_item)

        # Resize columns to fit content
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        delegate = BorderDelegate()
        table.setItemDelegate(delegate)

        # hover_filter = HoverEventFilter(table)
        # table.viewport().installEventFilter(hover_filter)

        layout.addWidget(table)
        self.process_tab.setLayout(layout)

    def initServicesTab(self):
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setRowCount(20)  # Set 20 rows
        table.setColumnCount(4)  # Set 4 columns
        table.setShowGrid(False)

        # Set column headers
        table.setHorizontalHeaderLabels(["Name", "PID", "Description", "Status"])

        # Add dummy data
        for i in range(20):
            table.setItem(i, 0, QTableWidgetItem(f"Service {i+1}"))
            pid = str(1000 + i) if i % 5 != 0 else ""  # Leave PID empty for some rows
            table.setItem(i, 1, QTableWidgetItem(pid))
            table.setItem(i, 2, QTableWidgetItem(f"Description for Service {i+1}"))
            status = "Running" if i % 2 == 0 else "Stopped"
            table.setItem(i, 3, QTableWidgetItem(status))

        # Set vertical headers invisible
        table.verticalHeader().setVisible(False)

        # Set vertical borders only
        table.setStyleSheet("QTableWidget::item { border-right: 1px solid #dcdcdc; }")

        # Resize columns to fit content
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(table)
        self.services_tab.setLayout(layout)

    def eventFilter(self, object, event):
        print("Caught event in the main window")
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManager()
    sys.exit(app.exec_())
