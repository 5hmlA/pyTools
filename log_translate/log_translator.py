import re

from data_struct import Log


# 用于解析多个tag  例子参考 BluetoothTranslator
class TagsTranslator(object):
    def __init__(self, tag_translators):
        self.tag_translators = tag_translators

    def translate(self, tag, msg):
        if tag in self.tag_translators:
            translator = self.tag_translators[tag]
            return translator(msg)
        return None


# 只解析一个tag
class TagTranslator(TagsTranslator):
    def __init__(self):
        super().__init__({self.tag(): self})

    def tag(self):
        pass

    def translate(self, tag, msg):
        return Log(translated=msg)


class DemoTagTranslator(TagTranslator):
    def tag(self):
        return "Netdiag"


class SysLogTranslator(object):
    def __init__(self, translators=None):
        # 这里是 TagsTranslator
        if translators is None:
            translators = []
        self.translators = translators

    def translate(self, string):
        # 系统日志
        # 03-21 21:31:45.534 12980 15281 I ActivityManager   : START 0 ooooo:
        syslog = re.search(r"(?P<time>\d+.*\.\d{3,}) .* [A-Z] (?P<tag>.*?) {0,}:(?P<msg>.*)", string)
        if syslog:
            tag = syslog.group("tag")
            msg = syslog.group("msg")
            time = syslog.group("time")
            for translator in self.translators:
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
