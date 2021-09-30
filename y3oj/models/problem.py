from y3oj.utils import render_markdown


class Problem:
    def __init__(self, id='', rank=0, title='', content=[], config={}):
        self.id = id
        self.rank = rank
        self.title = title
        self.content = content
        self.config = config
