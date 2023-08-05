import time


def consumer():
    r = 'i am start now!!!'
    while True:
        i = yield r
        print('consuming task %s' % i)
        r = '200 Done'


def producer(c):
    start_up = c.__next__() # 或者c.send(None) 启动生成器, 遇到yield 返回 重新来到这里
    print('start_up --> ', start_up)
    print('start_up is %s' % start_up)
    time.sleep(10)
    n = 5
    i = 0
    while i < n:
        i+=1
        print('producing task is %s' % i)
        res = c.send(i) # 生产了一个任务，通过 send(i) 把函数执行权切换到consumer，消费者接收任务处理， 此时consumer 的yield r 表达式等于send()的参数，即i=i
                        # 而send(i) 的返回值就由consumer的yield r产生，yield r 可以相当于return r 所以，res=“200 Done”
        print('consumer done ,res: %s' % res)

    c.close() # 不生产任务了，就关闭生成器


c = consumer()
producer(c)