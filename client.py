# client
import json
import sys
import logging
import time
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect

name = sys.argv[1]

logging.basicConfig(filename='%s.log' % name, level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p:')


def log(msg_from, msg_chat):
    print('%s says --> %s' % (msg_from, msg_chat))
    logging.info('%s says --> %s' % (msg_from, msg_chat))


class Friend:

    def __init__(self, url, timeout):
        self.url = url + '/chat'
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            log(name, e)
        else:
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            chat_msg = yield self.ws.read_message()
            if chat_msg is None:
                print('connecting closed.')
                log(name, 'connecting closed')
                self.ws = None
                break

            else:
                msg_from = json.loads(chat_msg).get('from', '')
                msg_chat = json.loads(chat_msg).get('chat', '')
                log(msg_from, msg_chat)

                if msg_chat == 'Hello ~':
                    msg_hello = {
                        'from': name,
                        'feel': 'Hello ~ George'
                    }
                    self.ws.write_message(json.dumps(msg_hello))
                    time.sleep(0.1)
                else:
                    input_feel = input('1.like;   2.unlike;   3.pass.   please chosen: ') or 3
                    msg_feeling = {
                        'from': name,
                        'feel': input_feel if input_feel in ['1', '2', '3'] else '3',
                        'chat': msg_chat
                    }
                    logging.info('from --> %s, %s feel --> %s, chat --> %s' %
                                 (msg_from, name, str(msg_feeling.get('feel', 3)), msg_chat))
                    self.ws.write_message(json.dumps(msg_feeling))
                    time.sleep(0.1)


if __name__ == '__main__':

    client = Friend('ws://127.0.0.1:8000', 5)

