#coding: utf-8
import multiprocessing
import threading
import time

def func_2(value):
    while True:
        print "value is {}".format(value)

def function(value):
    print "this is another process {}".format(value)
    what_thread = threading.Thread(target=what, args=(value,))
    what_thread.start()
    #time.sleep(5)
    print "end another process {}".format(value)

def func(msg):
    print "msg:", msg
    #pool = multiprocessing.Pool(4)
    for i in xrange(4):
        print "what"
        what = threading.Thread(target=func_2, args=(i,))
        what.start()
        #pool.apply_async(function, (i,))

        print "fuck"
    
    time.sleep(3)
    print "end"

if __name__ == "__main__":
    pool = multiprocessing.Pool(4)
    for i in xrange(10):
        msg = "hello %d" %(i)
        pool.apply_async(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print "Sub-process(es) done."