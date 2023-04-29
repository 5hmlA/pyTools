from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit

from read_log_file import LogReader
from PySide2.QtGui import QColor, Qt


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('连接日志解析工具')
        self.text_edit = QTextEdit('把日志文件拖入窗口', self)
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if not self.isMaximized():
                self.showMaximized()
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            print(url)
            if url.scheme() == 'file':
                filename = url.path()[1:]
                # parse the log file
                self.update_text(f"\n--------------{filename} 日志解析如下 --------------\n", QColor(Qt.green))
                self.parse_log_file(filename)
                event.acceptProposedAction()

    def parse_log_file(self, filename):
        # parse the log file, and return a string containing 10 random lines
        # for simplicity we just generate some random text here
        parse_log = LogReader(callback=self.callback_function)
        # parse_log.multiAnalyze(["E:\\log\\连接日志.txt"])
        parse_log.concurrency([filename])

    # 定义一个回调函数
    def callback_function(self, result):

        if result.error:
            self.update_text(result.__str__(), QColor(Qt.red))
        else:
            self.update_text(result.__str__(), QColor(Qt.black))

    def update_text(self, text, color):
        # update the text widget with the parsed log data
        # self.text_edit.clear()
        self.text_edit.setTextColor(color)
        self.text_edit.append(f"{text}\n")
        self.update()  # 刷新窗口


def main():
    app = QApplication([])
    window = MyMainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()



#  打包命令
# pyinstaller --name=log_translator --onefile --windowed ui.py
# -F, --onefile   产生单个的可执行文件
# -n NAME, --name NAME   指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字
# -w, --windowed, --noconsole   指定程序运行时不显示命令行窗口（仅对 Windows 有效）
# -i <FILE.ico>, --icon <FILE.ico>  指定icon

#  打包执行以下命令
# pyinstaller -n log_translator -F -w -i tools.ico ui.py


# pyinstaller --name=<your_exe_name> --onefile --windowed --add-data "<your_data_folder>;<your_data_folder>" <your_script_name>.py

# 上述命令中的选项说明：
# --name: 可执行文件名称。
# --onefile: 将整个项目打包为一个单独的可执行文件。
# --windowed: 隐藏控制台窗口，将打包的应用程序显示为GUI应用程序。
# --add-data: 添加项目资源，支持文件夹和文件，前面是资源路径，后面是输出路径，用分号进行分割。
# 执行上述命令后，会在项目目录下生成一个.spec文件，这个文件会告诉PyInstaller如何将项目打包成exe文件。