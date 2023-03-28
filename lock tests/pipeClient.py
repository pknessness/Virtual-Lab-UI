from shared import timeGlobal, mod
from random import randint
import time
from multiprocessing import Process

def f(lock):
    global timeGlobal
    timeGlobal = 3
    while(1):
        
        #print("a")
        #conn.send([42, None, 'hello'])
        #print("a",end="")
        #lock.acquire()
        mod(randint(0,10))
        #lock.release()
        time.sleep(1)
