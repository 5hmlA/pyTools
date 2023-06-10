# This is a sample Python script.
import os
import threading
from collections import deque
from os import cpu_count

from config import translates
from log_translator import *


# //必须定义在使用者前面
class LogReader(object):
    def __init__(self,
                 chunk_size=1024 * 1024 * 10,
                 process_num_for_log_parsing=cpu_count(),
                 callback=None,
                 translagors=translates):
        self.log_unparsed_queue = deque()  # 用于存储未解析日志
        self.log_line_parsed_queue = deque()  # 用于存储已解析日志行
        self.is_all_files_read = False  # 标识是否已读取所有日志文件
        self.process_num_for_log_parsing = process_num_for_log_parsing  # 并发解析日志文件进程数
        self.chunk_size = chunk_size  # 每次读取日志的日志块大小
        self.files_read_list = []  # 存放已读取日志文件
        self.log_parsing_finished = False  # 标识是否完成日志解析
        self.log_translators = translagors  # 翻译
        self.callback = callback

    def readFile(self, path="."):
        with open(path, "rb") as f:
            for fline in f:
                yield fline
            f.close()

    def analyze(self, path):
        # 分行读取数据
        for datas in self.readFile(path):
            # 对日志进行翻译
            try:
                str = datas.decode('ISO-8859-1')
                for translator in self.log_translators:
                    try:
                        result = translator.translate(str)
                        # 翻译后的日志存起来
                        if result:
                            print(result)
                            if self.callback:
                                self.callback(result)
                            break
                    except:
                        print(str)
            except:
                print("decode error")

    def concurrency(self, log_files):
        # 多线程 解析
        for file in log_files:
            abspath = os.path.abspath(file)
            print(abspath)
            threading_thread = threading.Thread(target=self.analyze, name="read_log_file", args=(abspath,))
            threading_thread.start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parse_log = LogReader()
    # parse_log.concurrency(["D:\\main_log_1__2023_0429_100141"])
    parse_log.concurrency(["./main_log_1__2023_0429_100141"])
