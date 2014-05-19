from entInfo import *
import threading
import time
import random

class ent_thread(threading.Thread):
    
    def __init__(self,i,id_f):
        threading.Thread.__init__(self)
        self.name = i
        self.tid = readlog('log/log%s'%(self.name))
        self.id_end = id_f
    
    def run(self):
        
        fbase = file('entBase/entBase%s.csv'%(self.name),'ab')
        basewriter = csv.writer(fbase)
        finvest = file('entInvest/entInvest%s.csv'%(self.name),'ab')
        investwriter = csv.writer(finvest)
        fperson = file('entPerson/entPerson%s.csv'%(self.name),'ab')
        personwriter = csv.writer(fperson)
        
        idcreator = eid()
        sear = search()
        hour_s = time.localtime().tm_hour#starting time of thread
        while(int(self.tid)<self.id_end):
            if(time.localtime().tm_hour >= (hour_s+1)%24):#Finish thread every one hour
                print 'Thread %s is Finished !'%(self.name)
                break
            self.tid += 1
            if(int(self.tid)<10000000):
                orderid = (8-len(str(self.tid)))*'0'+str(self.tid)
            else:
                orderid = str(self.tid)
#                 t = '50'+orderid
#             else:
#                 t = '50'+str(self.tid)
            idt = idcreator.mod(orderid)
#             print str(self.name)+':'+str(idt)
            link = sear.getLink(idt)
            if(len(link)>0):
                print str(self.name)+':'+str(idt)
                for l in link:
                    try:
                        info = entInfo(l)
                        basewriter.writerow(info.baseInf[1:])
                        
                        investinfo = info.inverstInf
                        if(len(investinfo)>0):
                            it = info.baseInf[1:3]
                            it.extend(investinfo[0])
                            investwriter.writerow(it)
                            for e in investinfo[1:]:
                                it = ['','']
                                it.extend(e)
                                investwriter.writerow(it)
                                
                        personinfo = info.personInf
                        if(len(personinfo)>0):
                            pt = info.baseInf[1:3]
                            pt.extend(list(personinfo[0]))
                            personwriter.writerow(pt)
                            for e in personinfo[1:]:
                                pt = ['','']
                                pt.extend(list(e))
                                personwriter.writerow(pt)
                    except AttributeError,e:
                        errorEnt(idt)
            log(self.tid,'log/log%s'%(self.name))
        fbase.close()
        finvest.close()
        fperson.close()

def hour_check():
    hour = time.localtime().tm_hour
    if(hour>9 and hour<17):
        return True
    else:
        return False

#Check whether all threads are temporary finished
def thread_check(threads):
    result = False
    for t in threads:
        result = result or t.isAlive()
    return result

#check whether all spyder tasks are finished
def finish_check(ids):
    result = True
    idt = []
    print len(ids)
    for i in range(len(ids)-1):
        if(int(readlog('log/log%s'%i))<ids[i+1]):
            result = False
            idt.append(i)
    return idt,result


def main():
    first = False
    number = 32
    num_day = 16
    id_s = 20200000#start serial number
    id_f = 21000000#end serial number
    ids = range(id_s,id_f,(id_f-id_s)/number)
    ids.append(id_f)
    mkdir('log')
    mkdir('entBase')
    mkdir('entInvest')
    mkdir('entPerson')
    input = raw_input('First time?(y or n)')
    if input == 'y':
        first = True
    if first:
        for i in range(number):
            log(ids[i], 'log/log%s'%i)
    threads_t = []
    
    while(True):
        (idt,finished)=finish_check(ids)
        if(finished):
            break
        threads = []
        for i in idt:
            t = ent_thread(i,ids[i+1])
            threads.append(t)

        if(hour_check()):
            while (True):
                print 'Threads are %s'%thread_check(threads_t)
                if not(thread_check(threads_t)):
                    break
                time.sleep(15)
            if(len(threads)<=num_day):
                threads_t = threads
            else:
                threads_t = random.sample(threads, num_day)
            for t in threads_t:
                print t.name
        else:
            threads_t = threads
        try:
            for t in threads_t:
                print 'Thread %s is started'%t.name
                t.start()
        except RuntimeError,e:
            print e
            print t.name
        time.sleep(3600)
    print 'Finished'
        
if __name__ == '__main__':
    main()
