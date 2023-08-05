# server
import json
import logging
import time

import tornado
import sqlite3
from tornado import websocket, ioloop, web

info = list(filter(lambda x: x != '', '''
将进酒
君不见黄河之水天上来，奔流到海不复回。
君不见高堂明镜悲白发，朝如青丝暮成雪。
人生得意须尽欢，莫使金樽空对月。
天生我材必有用，千金散尽还复来。
烹羊宰牛且为乐，会须一饮三百杯。
岑夫子，丹丘生，将进酒，杯莫停。
与君歌一曲，请君为我倾耳听。
钟鼓馔玉不足贵，但愿长醉不愿醒。
古来圣贤皆寂寞，惟有饮者留其名。
陈王昔时宴平乐，斗酒十千恣欢谑。
主人何为言少钱，径须沽取对君酌。
五花马、千金裘，呼儿将出换美酒，与尔同销万古愁。

行路难·其一
金樽清酒斗十千，玉盘珍羞直万钱。
停杯投箸不能食，拔剑四顾心茫然。
欲渡黄河冰塞川，将登太行雪满山。
闲来垂钓碧溪上，忽复乘舟梦日边。
行路难，行路难，多歧路，今安在？
长风破浪会有时，直挂云帆济沧海。

蜀道难
噫吁嚱，危乎高哉！
蜀道之难，难于上青天！
蚕丛及鱼凫，开国何茫然！
尔来四万八千岁，不与秦塞通人烟。
西当太白有鸟道，可以横绝峨眉巅。
地崩山摧壮士死，然后天梯石栈相钩连。
上有六龙回日之高标，下有冲波逆折之回川。
黄鹤之飞尚不得过，猿猱欲度愁攀援。
青泥何盘盘，百步九折萦岩峦。
扪参历井仰胁息，以手抚膺坐长叹。
问君西游何时还？畏途巉岩不可攀。
但见悲鸟号古木，雄飞雌从绕林间。
又闻子规啼夜月，愁空山。
蜀道之难，难于上青天，使人听此凋朱颜！
连峰去天不盈尺，枯松倒挂倚绝壁。
飞湍瀑流争喧豗，砯崖转石万壑雷。
其险也如此，嗟尔远道之人胡为乎来哉！(也如此 一作：也若此)
剑阁峥嵘而崔嵬，一夫当关，万夫莫开。
所守或匪亲，化为狼与豺。
朝避猛虎，夕避长蛇，磨牙吮血，杀人如麻。
锦城虽云乐，不如早还家。
蜀道之难，难于上青天，侧身西望长咨嗟！
'''.split('\n')))

logging.basicConfig(filename='MonkeyGeorge.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p:')


def log(msg_from, msg_chat):
    print('%s says --> %s' % (msg_from, msg_chat))
    logging.info('%s says --> %s' % (msg_from, msg_chat))


def init_db():
    log('init -->', 'db init begin')
    conn = sqlite3.connect('george.db')
    c = conn.cursor()
    c.execute("create table if not exists fri_sen_info "
              "(id integer not null primary key autoincrement, "
              "friend varchar (50),"
              "sentence TEXT,"
              "liked integer default 0,"
              "unliked integer default 0,"
              "passed integer default 0)")
    conn.commit()
    c.execute("select name from sqlite_master where type = 'table'")
    log('', str(c.fetchall()))
    conn.close()
    log('init --> ', 'db init done')


def insert_excep(s, s2):
    print('s --> ', s)
    print('s2 --> ', s2)
    conn = sqlite3.connect('george.db')
    c = conn.cursor()
    c.execute("create table if not exists conn_excep (id integer not null primary key autoincrement, "
              "errors text)")
    c.execute('''insert into conn_excep (errors) values ("%s")''' % (str(s) + str(s2)))
    conn.commit()
    conn.close()


class ChatWebSocket(websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        msg_hello = {
            'from': 'Monkey George',
            'chat': 'Hello ~'
        }

        self.write_message(msg_hello)

    def on_message(self, message):
        msg = json.loads(message)
        msg_from = msg.get('from', '')
        msg_feel = msg.get('feel', '')
        msg_chat = msg.get('chat', '')
        if msg_feel == 'Hello ~ George':
            log(msg_from, msg_feel)
            try:
                sentence = info.pop()
            except IndexError as e:
                sentence = 'all data has sent'
                logging.error(e)
            msg_rep = {
                'from': 'Monkey George',
                'chat': sentence
            }
            self.write_message(msg_rep)
        elif msg_from and msg_feel and msg_chat:
            print(msg_from, msg_feel, msg_chat)
            conn = sqlite3.connect('george.db')
            c = conn.cursor()
            sql = "insert into fri_sen_info (friend, sentence, '%s') values ('%s', '%s', '%i')"\
                  % ('liked', msg_from, msg_chat, int(msg_feel))
            print(sql)
            if msg_feel == '1':
                sql = "insert into fri_sen_info (friend, sentence, '%s') values ('%s', '%s', '%i')"\
                  % ('liked', msg_from, msg_chat, int(msg_feel))
            if msg_feel == '2':
                sql = "insert into fri_sen_info (friend, sentence, '%s') values ('%s', '%s', '%i')" \
                % ('unliked', msg_from, msg_chat, int(msg_feel))
            if msg_from == '3':
                sql = "insert into fri_sen_info (friend, sentence %s) values ('%s', '%s', '%i')" \
                % ('passed', msg_from, msg_chat, int(msg_feel))
            print('sql --> ', sql)
            c.execute(sql)
            log('george server', sql)
            conn.commit()
            conn.close()
            time.sleep(0.1)
            if msg_feel == '1':
                msg_rep = {
                    'from': 'Monkey George',
                    'chat': msg_chat
                }
                self.write_message(msg_rep)
            else:
                try:
                    sentence = info.pop()
                except IndexError as e:
                    sentence = 'all data has sent'
                    logging.error(e)
                msg_rep = {
                    'from': 'Monkey George',
                    'chat': sentence
                }
                self.write_message(msg_rep)

    def on_close(self):
        msg_goodbye = {
            'from': 'Monkey George',
            'chat': 'Goodbye ~'
        }
        self.write_message(msg_goodbye)

    def send_error(self, *args, **kwargs):
        logging.error(str(args))
        logging.error(str(kwargs))
        insert_excep(str(args), str(kwargs))

    def write_error(self, status_code, **kwargs):
        logging.error(str(status_code))
        logging.error(str(kwargs))
        insert_excep(str(status_code), str(kwargs))


class FeelRequesthandler(web.RequestHandler):

    def get(self):
        conn = sqlite3.connect('george.db')
        c = conn.cursor()

        html_str = ''

        c.execute("select friend, count(*) from fri_sen_info group by friend")
        res = c.fetchall()
        for i in res:
            html_str = html_str + '<h4>朋友：%s 回复次数最多：%i</h4>' % (i[0], i[1])

        c.execute("select friend, liked, sentence, count(sentence) from "
                  "fri_sen_info where liked = 1 group by sentence")
        res = c.fetchall()
        for i in res:
            html_str = html_str + '<h4>这个朋友是：%s 喜爱的句子是：%s 喜欢的次数是：%i</h4>' % (i[0], i[2], i[3])

        c.execute("select friend, unliked, sentence, count(sentence) from "
                  "fri_sen_info where unliked = 2 group by sentence")
        res = c.fetchall()
        for i in res:
            html_str = html_str + '<h4>这个朋友是：%s 不喜爱的句子是：%s 不喜欢的次数是：%i</h4>' % (i[0], i[2], i[3])

        c.execute("select friend, passed, sentence, count(sentence) from "
                  "fri_sen_info where passed = 3 group by sentence")
        res = c.fetchall()
        for i in res:
            html_str = html_str + '<h4>这个朋友是：%s 略过的句子是：%s 略过的次数是：%i</h4>' % (i[0], i[2], i[3])

        self.write(html_str)


if __name__ == '__main__':

    init_db()
    app = tornado.web.Application([
        (r'/chat', ChatWebSocket),
        (r'/rate', FeelRequesthandler)
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
