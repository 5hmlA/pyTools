import sys
from random import randint

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QMenu, QListWidgetItem, QAbstractItemView


class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        # self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            item = QListWidgetItem(path)
            item.setForeground(QBrush(QColor(randint(0, 255), randint(0, 255), randint(0, 255))))
            self.addItem(item)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.list_widget = MyListWidget()
        self.setCentralWidget(self.list_widget)
        self.setAcceptDrops(True)
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")

        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear_list)
        file_menu.addAction(clear_action)

        separator_action = QAction("Add Separator", self)
        separator_action.triggered.connect(self.add_separator)
        edit_menu.addAction(separator_action)

    def clear_list(self):
        self.list_widget.clear()

    def add_separator(self):
        item = QListWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignCenter)
        item.setText("--------------------")
        self.list_widget.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
