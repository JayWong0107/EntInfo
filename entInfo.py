# -*- coding: UTF-8 -*-
import urllib2
import re
import csv
import httplib
import time
import socket

def getContent(url):
    
    my_headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
           }
    tout = 50
    content = None
    while True:
        try:
            req = urllib2.Request(url,headers=my_headers)
            html = urllib2.urlopen(req,timeout=tout)
            content = html.read()
            html.close()
            break  
        except urllib2.URLError,e:
            print e
            time.sleep(10)
        except socket.timeout,e:
            print e
            tout += 50
            if(tout > 200):
                break
        except socket.error,e:
            print e
            time.sleep(10)
        except httplib.BadStatusLine,e:
            print 'Get None Info'
            break
        except ValueError,e:
            print e
#             url = url.replace('..','http://gsxt.gdgs.gov.cn')
            break
    return content
    
    

class entInfo:
    
    def __init__(self,url):
        if(url != None):
            self.content = getContent(url)
            if self.content != None:
                self.getbaseInfo()
                self.getinvestInfo()
                self.getPerson()
    
    def getPerson(self,content=None):
        content = content or self.content
        personp = '<td style="text-align:center;">\d{1,2}</td><td>(.*?)</td><td>(.*?)</td>'
        info = re.compile(personp, re.S)
        self.personInf = re.findall(info, content)
        return self.personInf
    
    def getbaseInfo(self,content=None):
        content = content or self.content
        infop = '<span id=".*?">(.*?)</span>'
        infor = re.compile(infop, re.S)
        self.baseInf = re.findall(infor, content)
        if(len(self.baseInf)<14):self.baseInf=self.baseInfosort(self.baseInf)
        self.baseInf[1] += ' '
        return self.baseInf[1:]
    
    def getInvestDeatail(self,content = None):
        content = content or self.content
        linkp = r'EntSHDetail.aspx\?rid=([A-Za-z0-9]{32})'
        linkr = re.compile(linkp, re.S)
        link = re.findall(linkr,content)
        self.investmoney = []
        for l in link:
            l = 'http://www.szcredit.com.cn/web/GSZJGSPT/EntSHDetail.aspx?rid='+l
            content_d = getContent(l)
            dp = r'<span id="CapAmt1">(.*?)</span>'
            dr = re.compile(dp, re.S)
            detail = re.findall(dr, content_d)
            self.investmoney.append(detail[0])
        return self.investmoney

    def baseInfosort(self,info):
        t = ['']*14
        t[:5] = info[:5]
        t[6] = info[6]
        t[7] = info[5]
        t[8] = info[10]
        t[9] = info[9]
        t[10] = info[8]
        t[11:] = info[10:]
        return t
    
    def getinvestInfo(self,content=None):
        t = content or self.content
        investp = r'<tr>(.*?)<td><a href=.*?target="_blank">.*?</a>'
        investr = re.compile(investp,re.S)
        info = re.findall(investr, t)
    
        self.inverstInf =[]
        ip = '<td>(.*?)</td>'
        ir = re.compile(ip, re.S)
        for i in range(len(info)):
            t = re.findall(ir, info[i])
            if(i == 0):
                self.inverstInf.append(t[-4:])
            else:
                self.inverstInf.append(t)   
        investmoney = self.getInvestDeatail()
        for i in range(len(self.inverstInf[1:])):
            self.inverstInf[i+1][-1] += ' '
            self.inverstInf[i+1].append(investmoney[i])
        return self.inverstInf[1:]


class search:
    def __init__(self):
        self.link = None
        
    def getLink(self,eid):
        url = 'http://gsxt.gdgs.gov.cn/CheckEntContext/showInfo.html?textfield='+str(eid)
        self.content = getContent(url)
        lp = 'QyxyDetail.aspx\?rid=([A-Za-z0-9]{32})'
        lr = re.compile(lp, re.S)
        self.link = re.findall(lr, self.content)
        for i in range(len(self.link)):
            self.link[i] = 'http://www.szcredit.com.cn/web/GSZJGSPT/QyxyDetail.aspx?rid='+self.link[i]           
        return self.link
    
    def getshortinfo(self,content=None):
        content = content or self.content
        t = []
        namep = r'target=_blank>(.*?)</a> </dt>'
        namer = re.compile(namep)
        nameinfo = re.findall(namer,content)
        t.extend(nameinfo)
    
        shortp = r'<span>(.*?)</span>'
        sr = re.compile(shortp, re.S)
        sinfo = re.findall(sr, content)
        t.extend(sinfo)
    
        self.info = ['']*14
        self.info[0:2] = t[0:2]
        self.info[2] = t[0]
        self.info[4] = t[2]
        self.info[10] = t[3]
        return self.info

class eid:
    def __init__(self):
        self.eid = None
    
    def tolist(self,tid):
        t = str(tid)
        list_t = []
        for i in range(len(t)):
            list_t.append(int(t[i]))
        return list_t
    
    def mod(self,orderid,areaid=440301):
        id_l = str(areaid)+str(orderid)
        t = self.tolist(id_l)
        p = 10
        for i in range(len(t)):
            p += t[i]
            p = p%10
            if(p == 0):p=10
            p = (p*2)%11
        p = (11 - p)%10
        t.append(p)
        id_t = ''
        for e in t:
            id_t += str(e)
        self.eid = id_t
        return id_t
        
def log(eid,fname='log'):
    fw = open(fname,'wb')
    fw.write(str(eid))
    fw.close()
    
def errorEnt(eid):
    fw = open('errorEnt.txt','ab')
    fw.write(str(eid)+'\n')
    fw.close()

def readlog(fname='log'):
    fr = open(fname,'rb')
    eid = fr.readline()
    fr.close()
    return int(eid.rstrip())

def listconvert(p):
    t = []
    for e in p:
        t.append(e.decode('utf8').encode('gbk'))
    return t
        
    
def main():
#     ft = raw_input('First time or continue(y or n)?')
    firstTime = False
#     if ft == 'y':
#         firstTime = True
    
    ferror = open('errorEnt.txt','ab')
    fbase = file('entBase.csv','ab')
    basewriter = csv.writer(fbase)
    finvest = file('entInvest.csv','ab')
    investwriter = csv.writer(finvest)
    fperson = file('entPerson.csv','ab')
    personwriter = csv.writer(fperson)
    
    if firstTime:
        log_t = raw_input('ID start from(<8 numbers):')
        while(len(log_t)>8):
            log_t = raw_input('ID start from(<8 numbers):')
        log(log_t)
        bt = ['注册号','名称','类型','法定代表人','注册资本(万元)','成立日期','住所','营业限期自','营业限期至','登记机关','发照日期','经营状态','经营范围','']
        baselist = listconvert(bt)
        it = ['注册号','名称','投资人类型','投资人','证照类型','证照号码','投资金额']
        investlist = listconvert(it)
        pt = ['注册号','名称','姓名','职务']
        personlist =listconvert(pt)
        basewriter.writerow(baselist)
        investwriter.writerow(investlist)
        personwriter.writerow(personlist)

    count = readlog()
    idcreator = eid()
    while count<30309950:
        
        count +=1
#         print count
        orderid = (8-len(str(count)))*'0'+str(count)
        idt = idcreator.mod(orderid)
        sear = search()
        link = sear.getLink(idt)
        if(len(link)>0):
            print idt
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
                        
                    log(count)
                except AttributeError,e:
                    baseinfo = sear.getshortinfo()
                    basewriter.writerow(baseinfo)
                    ferror.write(str(idt)+'\n')
        else:
            pass
#             check = raw_input('To continue?(y or n)')
#             if(check!='y'):break
    fbase.close()
    finvest.close()
    fperson.close()
    ferror.close()
    
if __name__ == '__main__':
    main()