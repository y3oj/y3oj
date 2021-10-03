encoding = 'gbk'

class InputPipeError(Exception):
    pass


class OutputPipeError(Exception):
    pass


class InputPipe(object):
    def _send(self, string):
        self.pipe.write(string.encode(encoding))
        self.pipe.flush()

    def send(self, text, end='\n'):
        self._send(text + end)

    def __init__(self, pipe):
        assert pipe.writable()
        self.pipe = pipe
        # print('input', dir(pipe))


class OutputPipe(object):
    def _recv(self):
        self.cache += self.pipe.read1().decode(encoding)

    def _reset_cache(self):
        self.cache = ''
        self.pointer = 0

    def recv(self):
        self._recv()
        res = self.cache[self.pointer:]
        self._reset_cache()
        return res

    def recv_int(self):
        self._recv()
        if self.pointer == len(self.cache):
            raise OutputPipeError('No integers more.')
        res = 0
        while self.pointer < len(self.cache):
            c = self.cache[self.pointer]
            if 48 <= ord(c) and ord(c) <= 57:
                res = res * 10 + int(c)
                self.pointer += 1
            else:
                break
        if self.pointer == len(self.cache):
            self._reset_cache()
        return res

    def __init__(self, pipe):
        assert pipe.readable()
        self.pipe = pipe
        self._reset_cache()
        # print('output', dir(pipe))
