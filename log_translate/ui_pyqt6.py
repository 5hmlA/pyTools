import sys
import traceback

from PyQt6.QtGui import QAction, QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QAbstractItemView

from data_struct import Log
from read_log_file import LogReader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖放文件示例")
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setCentralWidget(self.list_widget)
        self.setAcceptDrops(True)
        self.create_menu()
        self.log_reader = LogReader()
        self.log_reader.log_stream.subscribe_(lambda log: {
            self.list_widget.addItem(self.addItemFromLog(log))
        })

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
            if not self.isMaximized():
                self.showMaximized()
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            # f-string 可以使用 {变量} 语法将表达式嵌入到字符串中
            self.list_widget.addItem(f"\n--------------{file} 日志解析如下 --------------")
            try:
                self.log_reader.concurrency([file])
            except Exception as e:
                item = QListWidgetItem(traceback.format_exc())
                item.setForeground(QBrush(QColor("red")))
                self.list_widget.addItem(item)
            # for i in range(100):

    def addItemFromLog(self, log: Log):
        item = QListWidgetItem(log.__str__())
        item.setForeground(QBrush(QColor(log.level.color())))
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
