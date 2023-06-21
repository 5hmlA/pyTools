import sys
from random import randint

from PyQt6.QtGui import QAction, QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QAbstractItemView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖放文件示例")
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setCentralWidget(self.list_widget)
        self.setAcceptDrops(True)
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        action = menu_bar.addMenu("操作")

        clear_action = QAction("清空", self)
        clear_action.triggered.connect(self.clear_list)
        action.addAction(clear_action)

        separator_action = QAction("分割线", self)
        separator_action.triggered.connect(self.add_separator)
        action.addAction(separator_action)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            # for i in range(100):
            item = QListWidgetItem(path)
            item.setForeground(QBrush(QColor(randint(0, 255), randint(0, 255), randint(0, 255))))
            self.list_widget.addItem(item)

    def clear_list(self):
        self.list_widget.clear()

    def add_separator(self):
        self.list_widget.addItem("--" * 40)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
