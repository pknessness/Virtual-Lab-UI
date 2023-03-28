from multiprocessing import Process, Pipe
import pipeClient

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=pipeClient.f, args=(child_conn,))
    p.start()
    while(1):
        print(parent_conn.readable)
        if(not parent_conn.readable):
            print (parent_conn.recv())   # prints "[42, None, 'hello']"
        print ("AAA")
    p.join()