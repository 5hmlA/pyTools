import random

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QListWidget, \
    QListWidgetItem, QAbstractItemView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖放文件示例")
        self.resize(400, 300)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setAcceptDrops(True)
        self.setCentralWidget(self.list_widget)
        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = QMenuBar()
        file_menu = QMenu("文件", menu_bar)
        clear_action = QAction("清空列表", file_menu)
        clear_action.triggered.connect(self.clear_list)
        line_action = QAction("增加分割线", file_menu)
        line_action.triggered.connect(self.add_line)
        file_menu.addAction(clear_action)
        file_menu.addAction(line_action)
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

    def clear_list(self):
        self.list_widget.clear()

    def add_line(self):
        self.list_widget.addItem("-" * 40)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            item = self.createItemFromUrl(url)
            self.list_widget.addItem(item)

    def createItemFromUrl(self, url):
        item = QListWidgetItem(url.toLocalFile())
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        item.setForeground(color)
        return item


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
