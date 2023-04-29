import re
from abc import ABC

from config import translates


class TagsTranslator(object):
    def __init__(self, tag_translators=translates):
        self.tags = dict()
        for tag_translator in tag_translators:
            self.tags[tag_translator.tag()] = tag_translator

    def translate(self, tag, msg):
        if self.tags:
            return self.tags[tag](msg)
        return None


class TagTranslator(ABC):
    def tag(self):
        pass

    def translate(self, msg):
        pass


class TranslateTags(object):
    def __init__(self, tags={}):
        self.tags = {}

    def translate(self, tag, msg):
        translator = self.tags[tag]
        if translator:
            return translator.tagTranslator(msg)
        return None


class SysLogTranslator(object):
    def __init__(self, translators=[TagsTranslator()]):
        self.translators = translators

    def translate(self, string):
        # 系统日志
        # 03-21 21:31:45.534 12980 15281 I ActivityManager   : START 0 ooooo:
        syslog = re.search(r"(?P<time>\d+.*\.\d{3,}) .* [A-Z] (?P<tag>.*?) {0,}:(?P<msg>.*)", string)
        if syslog:
            time = syslog.group("time")
            tag = syslog.group("tag")
            msg = syslog.group("msg")
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
