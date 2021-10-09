import json
import asyncio
import websockets
from threading import Thread

from y3oj import db, config, logger
from y3oj.models import Submission


class Judger:
    def recv(self, msg):
        self.logger.debug('recv:', json.dumps(msg))
        if msg['type'] == 'judge-result':
            data = msg['data']
            submission = db.session.query(Submission).filter_by(id=msg['id']).first()
            submission.status = data['status']
            submission.time = data['time'] if 'time' in data else 0
            submission.memory = data['memory'] if 'memory' in data else 0
            submission.details = data['details']
            db.session.commit()

    def submit(self, submission: Submission):
        msg = {
            'type': 'submit',
            'data': {
                'id': submission.id,
                'user': submission.user,
                'problem': submission.problem,
                'code': submission.code,
            },
        }
        self.logger.debug('send', msg)
        asyncio.run_coroutine_threadsafe(self.ws.send(json.dumps(msg)),
                                         self.loop)

    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        self.logger = logger.module('judger')
        self.active = False

        async def asyncio_entry():
            self.ws = await websockets.connect(f'ws://{self.host}:{self.port}')
            self.logger.debug('websocket-client: connected.')
            self.active = True
            while True:
                response = await self.ws.recv()
                self.recv(json.loads(response))

        def asyncio_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=asyncio_loop,
                             daemon=True,
                             args=(self.loop, ))
        self.thread.start()
        asyncio.run_coroutine_threadsafe(asyncio_entry(), self.loop)


judger = Judger(host=config.judger.remote_host, port=config.judger.port)