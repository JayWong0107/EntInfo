from entInfo import *
import threading

class ent_thread(threading.Thread):
    
    def __init__(self,i):
        threading.Thread.__init__(self)
        self.name = i
        self.tid = readlog('log%s'%(self.name))
    
    def run(self):
        
        fbase = file('entBase%s.csv'%(self.name),'ab')
        basewriter = csv.writer(fbase)
        finvest = file('entInvest%s.csv'%(self.name),'ab')
        investwriter = csv.writer(finvest)
        fperson = file('entPerson%s.csv'%(self.name),'ab')
        personwriter = csv.writer(fperson)
        
        idcreator = eid()
        sear = search()
        while(int(self.tid)<99999):
            self.tid += 1
            if(int(self.tid)<10000):
                orderid = (5-len(str(self.tid)))*'0'+str(self.tid)
                t = '10'+str(self.name)+orderid
            else:
                t = '10'+str(self.name)+str(self.tid)
            idt = idcreator.mod(t)
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
            log(self.tid,'log%s'%(self.name))
        fbase.close()
        finvest.close()
        fperson.close()

def main():
    number = 10
    threads = []
    for i in range(number):
        log(0,'log%s'%i)
        t = ent_thread(i)
        threads.append(t)
    
    for t in threads:
        t.start()
        
if __name__ == '__main__':
    main()
