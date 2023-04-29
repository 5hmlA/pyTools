class Log(object):
    def __init__(self, time="", process="", origin="", translated="", error=False, type=""):
        self.time = time
        self.process = process
        self.origin = origin
        self.translated = translated
        self.error = error
        self.type = type

    def __str__(self):
        return self.time + ">" + self.process + ">" + self.translated
        # return self.time + ">" + self.process + ">" + self.origin_msg + ">" + self.translated_msg
