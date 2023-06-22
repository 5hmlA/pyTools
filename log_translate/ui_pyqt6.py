import sys
import traceback

from PyQt6.QtGui import QAction, QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QAbstractItemView

from data_struct import Log
from read_log_file import LogReader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖日志解析")
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setCentralWidget(self.list_widget)
        self.setAcceptDrops(True)
        self.create_menu()
        self.log_reader = LogReader()
        self.log_reader.log_stream.subscribe_(lambda log: {
            self.list_widget.addItem(self.addItemFromLog(log))
        })
        self.list_widget.addItem("💫 💭 把文件拖入到窗口开始解析日志 💭 💫")

    def create_menu(self):
        menu_bar = self.menuBar()
        action = menu_bar.addMenu("操作")

        clear_action = QAction("清空", self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear_list)
        action.addAction(clear_action)

        separator_action = QAction("分割线", self)
        separator_action.setShortcut('Ctrl+L')
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
            self.list_widget.clear()
            self.list_widget.addItem(f"\n👇👇👇👇👇👇👇👇 {file} 💥 日志解析如下 👇👇👇👇👇👇👇👇")
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

#  打包命令
# pyinstaller --name=log_translator --onefile --windowed ui_pyqt6.py
# -F, --onefile   产生单个的可执行文件
# -n NAME, --name NAME   指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
# -w, --windowed, --noconsole   指定程序运行时不显示命令行窗口（仅对 Windows 有效）
# -i <FILE.ico>, --icon <FILE.ico>  指定icon

#  打包执行以下命令
# pyinstaller -n log_translator -F -w -i tools.ico ui_pyqt6.py

# pip install PyInstaller
# pyinstaller --name=<your_exe_name> --onefile --windowed --add-data "<your_data_folder>;<your_data_folder>" <your_script_name>.py

# 上述命令中的选项说明：
# --name: 可执行文件名称。
# --onefile: 将整个项目打包为一个单独的可执行文件。
# --windowed: 隐藏控制台窗口，将打包的应用程序显示为GUI应用程序。
# --add-data: 添加项目资源，支持文件夹和文件，前面是资源路径，后面是输出路径，用分号进行分割。
# 执行上述命令后，会在项目目录下生成一个.spec文件，这个文件会告诉PyInstaller如何将项目打包成exe文件。
