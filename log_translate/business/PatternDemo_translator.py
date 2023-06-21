import re

from log_translator import *
from data_struct import Log


class TranslatorPartternDemoTranslator(TagPatternTranslator):
    def __init__(self):
        super().__init__({
            ".*TaskManager": activity_task_translator
        })


def activity_task_translator(tag, msg):
    return Log(translated=" ------ %s > %s----- " % (tag, msg))


if __name__ == '__main__':
    print(re.compile(".*Task").match("aaTas8km"))
    print(TranslatorPartternDemoTranslator().translate("AcTaskManager", "你好"))
