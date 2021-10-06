from y3oj import config


class Judger:
    def __init__(self, host, port):
        self.host = host
        self.port = port


judger = Judger(host=config.judger.remote_host, port=config.judger.port)
