import traceback

from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QListWidget, \
    QListWidgetItem, QAbstractItemView

from data_struct import Log
from read_log_file import LogReader


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
        self.log_reader = LogReader()
        self.log_reader.log_stream.subscribe_(lambda log: {
            self.addItemFromLog(log)
        })

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        action_menu = QMenu("操作")
        clear_action = QAction("清空列表")
        clear_action.triggered.connect(self.clear_list)
        line_action = QAction("增加分割线")
        line_action.triggered.connect(self.add_line)

        action_menu.addAction(clear_action)
        action_menu.addAction(line_action)
        menu_bar.addMenu(action_menu)
        self.setMenuBar(menu_bar)

    def clear_list(self):
        self.list_widget.clear()

    def add_line(self):
        self.list_widget.addItem("-" * 40)

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
            self.list_widget.addItem(f"\n--------------{file} 日志解析如下 --------------\n")
            try:
                self.log_reader.concurrency([file])
            except Exception as e:
                item = QListWidgetItem(traceback.format_exc())
                item.setForeground(QColor("red"))
                self.list_widget.addItem(item)

    def addItemFromLog(self, log: Log):
        item = QListWidgetItem(log.__str__())
        color = QColor(log.level.color())
        item.setForeground(color)
        self.list_widget.addItem(item)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
