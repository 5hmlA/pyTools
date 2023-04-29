# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# import re
# import time
# from datetime import datetime
# from joblib import Parallel, delayed, parallel_backend
# from collections import deque
# from multiprocessing import cpu_count
# import threading
#
#
# class LogParser(object):
#     def __init__(self, chunk_size=1024 * 1024 * 10, process_num_for_log_parsing=cpu_count()):
#         self.log_unparsed_queue = deque()  # 用于存储未解析日志
#         self.log_line_parsed_queue = deque()  # 用于存储已解析日志行
#         self.is_all_files_read = False  # 标识是否已读取所有日志文件
#         self.process_num_for_log_parsing = process_num_for_log_parsing  # 并发解析日志文件进程数
#         self.chunk_size = chunk_size  # 每次读取日志的日志块大小
#         self.files_read_list = []  # 存放已读取日志文件
#         self.log_parsing_finished = False  # 标识是否完成日志解析
#
#     def read_in_chunks(self, filePath, chunk_size=1024 * 1024):
#         """
#         惰性函数（生成器），用于逐块读取文件。
#         默认区块大小：1M
#         """
#
#         with open(filePath, 'r', encoding='utf-8') as f:
#             while True:
#                 chunk_data = f.read(chunk_size)
#                 if not chunk_data:
#                     break
#                 yield chunk_data
#
#     def read_log_file(self, logfile_path):
#         '''
#         读取日志文件
#         这里假设日志文件都是文本文件，按块读取后，可按换行符进行二次切分，以便获取行日志
#         '''
#
#         temp_list = []  # 二次切分后，头，尾行日志可能是不完整的，所以需要将日志块头尾行日志相连接，进行拼接
#         for chunk in self.read_in_chunks(logfile_path, self.chunk_size):
#             log_chunk = chunk.split('\n')
#             temp_list.extend([log_chunk[0], '\n'])
#             temp_list.append(log_chunk[-1])
#             self.log_unparsed_queue.append(log_chunk[1:-1])
#         self.log_unparsed_queue.append(''.join(temp_list).split('\n'))
#         self.files_read_list.remove(logfile_path)
#
#     def start_processes_for_log_parsing(self):
#         '''启动日志解析进程'''
#
#         with parallel_backend("multiprocessing", n_jobs=self.process_num_for_log_parsing):
#             Parallel(require='sharedmem')(delayed(self.parse_logs)() for i in range(self.process_num_for_log_parsing))
#
#         self.log_parsing_finished = True
#
#     def parse_logs(self):
#         '''解析日志'''
#
#         method_url_re_pattern = re.compile('(HEAD|POST|GET)\s+([^\s]+?)\s+', re.DOTALL)
#         url_time_taken_extractor = re.compile('HTTP/1\.1.+\|(.+)\|\d+\|', re.DOTALL)
#
#         while self.log_unparsed_queue or self.files_read_list:
#             if not self.log_unparsed_queue:
#                 continue
#             log_line_list = self.log_unparsed_queue.popleft()
#             for log_line in log_line_list:
#                 #### do something with log_line
#                 if not log_line.strip():
#                     continue
#
#                 res = method_url_re_pattern.findall(log_line)
#                 if not res:
#                     print('日志未匹配到请求URL，已忽略：\n%s' % log_line)
#                     continue
#                 method = res[0][0]
#                 url = res[0][1].split('?')[0]  # 去掉了 ?及后面的url参数
#
#                 # 提取耗时
#                 res = url_time_taken_extractor.findall(log_line)
#                 if res:
#                     time_taken = float(res[0])
#                 else:
#                     print('未从日志提取到请求耗时，已忽略日志：\n%s' % log_line)
#                     continue
#
#                 # 存储解析后的日志信息
#                 self.log_line_parsed_queue.append({'method': method,
#                                                    'url': url,
#                                                    'time_taken': time_taken,
#                                                    })
#
#     def collect_statistics(self):
#         '''收集统计数据'''
#
#         def _collect_statistics():
#             while self.log_line_parsed_queue or not self.log_parsing_finished:
#                 if not self.log_line_parsed_queue:
#                     continue
#                 log_info = self.log_line_parsed_queue.popleft()
#                 # do something with log_info
#
#         with parallel_backend("multiprocessing", n_jobs=1):
#             Parallel()(delayed(_collect_statistics)() for i in range(1))
#
#     def run(self, file_path_list):
#         # 多线程读取日志文件
#         for file_path in file_path_list:
#             thread = threading.Thread(target=self.read_log_file,
#                                       name="read_log_file",
#                                       args=(file_path,))
#             thread.start()
#             self.files_read_list.append(file_path)
#
#         # 启动日志解析进程
#         thread = threading.Thread(target=self.start_processes_for_log_parsing, name="start_processes_for_log_parsing")
#         thread.start()
#
#         # 启动日志统计数据收集进程
#         thread = threading.Thread(target=self.collect_statistics, name="collect_statistics")
#         thread.start()
#
#         start = datetime.now()
#         while threading.active_count() > 1:
#             print('程序正在努力解析日志...')
#             time.sleep(0.5)
#
#         end = datetime.now()
#         print('解析完成', 'start', start, 'end', end, '耗时', end - start)
#
#
# if __name__ == "__main__":
#     log_parser = LogParser()
#     log_parser.run(['access.log', 'access2.log'])