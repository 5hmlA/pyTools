import re

from data_struct import Log


# 通过正则表达式匹配tag解析
class TagPatternTranslator(object):
    def __init__(self, pattern_translators):
        self.pattern_translators = pattern_translators

    def translate(self, tag, msg):
        for pattern in self.pattern_translators:
            match = re.compile(pattern, tag)
            if match:
                return self.pattern_translators[pattern](msg)
        return None


# 字符串匹配tag  例子参考 BluetoothTranslator
class TagStrTranslator(object):
    def __init__(self, str_translators):
        self.str_translators = str_translators

    def translate(self, tag, msg):
        if tag in self.str_translators:
            translator = self.str_translators[tag]
            return translator(msg)
        return None


class SysLogTranslator(object):
    def __init__(self, tag_translators=None):
        # 这里是 TagStrTranslator
        if tag_translators is None:
            tag_translators = []
        self.tag_translators = tag_translators

    def translate(self, string):
        # 系统日志
        # 03-21 21:31:45.534 12980 15281 I ActivityManager   : START 0 ooooo:
        syslog = re.search(r"(?P<time>\d+.*\.\d{3,}) .* [A-Z] (?P<tag>.*?) {0,}:(?P<msg>.*)", string)
        if syslog:
            tag = syslog.group("tag")
            msg = syslog.group("msg")
            time = syslog.group("time")
            for translator in self.tag_translators:
                show = translator.translate(tag, msg)
                if show:
                    show.time = time
                    show.oring = msg
                    return show
        return None


if __name__ == '__main__':
    result = re.search("device: (.*?),", "connect() - device: 34:47:9A:31:52:CF, auto: false, eattSupport: false")
    print(result.group(1))
    result = re.search("(?<=\*).*", "onReCreateBond: 24:*:35:06")

    # (?<=A).+?(?=B) 匹配规则A和B之间的元素 不包括A和B
    #
    print(result.group())
