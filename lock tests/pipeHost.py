from multiprocessing import Process, Lock
import pipeClient, time
from shared import timeGlobal, mod

if __name__ == '__main__':
    lock = Lock()
    pipeClient.f(lock)
    
    while(1):
        #lock.acquire()
        print(timeGlobal)
        #lock.release()
    #.join()
    