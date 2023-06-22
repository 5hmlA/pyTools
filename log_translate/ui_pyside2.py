import traceback

from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QListWidget, \
    QListWidgetItem, QAbstractItemView

from data_struct import Log
from read_log_file import LogReader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖日志解析")
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
        self.list_widget.addItem("💫 💭 把文件拖入到窗口开始解析日志 💭 💫")

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        action_menu = QMenu("操作", self)
        clear_action = QAction("清空列表", self)
        clear_action.setShortcut('Ctrl+O')
        clear_action.triggered.connect(self.clear_list)
        line_action = QAction("增加分割线", self)
        line_action.setShortcut('Ctrl+L')
        line_action.triggered.connect(self.add_line)

        action_menu.addAction(clear_action)
        action_menu.addAction(line_action)
        menu_bar.addMenu(action_menu)

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
            self.list_widget.clear()
            self.list_widget.addItem(f"\n👇👇👇👇👇👇👇👇 {file} 💥 日志解析如下 👇👇👇👇👇👇👇👇")
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

#  打包命令
# pyinstaller --name=log_translator --onefile --windowed ui_pyside2.py
# -F, --onefile   产生单个的可执行文件
# -n NAME, --name NAME   指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
# -w, --windowed, --noconsole   指定程序运行时不显示命令行窗口（仅对 Windows 有效）
# -i <FILE.ico>, --icon <FILE.ico>  指定icon

#  打包执行以下命令
# pyinstaller -n log_translator -F -w -i tools.ico ui_pyside2.py

# pip install PyInstaller
# pyinstaller --name=<your_exe_name> --onefile --windowed --add-data "<your_data_folder>;<your_data_folder>" <your_script_name>.py

# 上述命令中的选项说明：
# --name: 可执行文件名称。
# --onefile: 将整个项目打包为一个单独的可执行文件。
# --windowed: 隐藏控制台窗口，将打包的应用程序显示为GUI应用程序。
# --add-data: 添加项目资源，支持文件夹和文件，前面是资源路径，后面是输出路径，用分号进行分割。
# 执行上述命令后，会在项目目录下生成一个.spec文件，这个文件会告诉PyInstaller如何将项目打包成exe文件。
