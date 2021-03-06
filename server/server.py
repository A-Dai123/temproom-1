# -*- coding=utf-8 -*-


"""
file: temproom_server.py
"""
import threading
import DataBaseRelated
import recv
class MyThread(threading.Thread):

    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def check():
    total=[]
    cur,conn=DataBaseRelated.ini()
    numberlist=DataBaseRelated.return_roomnumberlist(cur)
    amountlist=DataBaseRelated.return_useramountlist(cur)

    for i in range(len(amountlist)):
        if amountlist[i] >=2:
            users=DataBaseRelated.curretroomusers(numberlist[i],cur)
            total.append((users,numberlist[i]))
    return total
total=check()
t=[]
def trans1(client):
    return recv.recv(client)


def trans2(k,client,t):
    for j in t:
        if j!=t[k]:
            while 1:
                if not j.isAlive():
                    break
            recv.send(client,j.get_result())

for i in total:
	amount=len(i[0])#TCP问题很大啊感觉
    print(amount)
    s=recv.server_ini（amount)
    clients=recv.server_connect(amount,s)
    for j in range(amount):
        th=MyThread(target=trans1,args=clients[j][0])
        t.append(th)
        t[j].start()
    for k in range(amount):
        th2=threading.thread(target=trans2,args=(k,clients[k][0],t))
        th2.start()




#print(clients[0][1])

#username=recv.recv(clients[0][0])
#print('用户为'+username)
#recv.send(clients[0][0],username)
#clients[0][0].close()
