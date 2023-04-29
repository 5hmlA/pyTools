# 这是一个示例 Python 脚本。
import os
import re
import shutil


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

def traverse_files(folder_path):
    folder_path = os.path.abspath(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            old_file = os.path.join(root, file)
            result = re.search("^\d+", file)
            if result:
                num = result.group()
                if len(num) == 1:
                    new_name = file.replace(num, "0%s" % num, 1)
                else:
                    new_name = file
                new_file = os.path.join(folder_path, new_name)
                if not os.path.exists(new_file):
                    if new_file != old_file:
                        os.rename(old_file, new_file)
                else:
                    print("%s 已经存在" % new_file)
            # shutil.rename()


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。

    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    traverse_files('.')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
