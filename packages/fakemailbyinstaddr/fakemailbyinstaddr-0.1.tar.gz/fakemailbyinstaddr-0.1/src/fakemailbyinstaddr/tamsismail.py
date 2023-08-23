import requests,re,os
from random import choice
from bs4 import BeautifulSoup as par

def manual(mail):
        ses=requests.Session()
        ses.get("https://m.kuku.lu/index.php")
        user=""
        login2 = par(ses.get("https://m.kuku.lu/id.php").text,"html.parser")
        for c in login2.find_all("script"):
            if 'data: "action=addMailAddrByAuto' in str(c):
                ff=str(par(ses.get(f"https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t={re.search('t=(.*?)&',str(c)).group(1)}&csrf_token_check={re.search('csrf_token_check=(.*?)&',str(c)).group(1)}&newdomain={mail}&newuser={user}&recaptcha_token=&").text,"html.parser")).replace("OK:","")
                cok = (";").join([ "%s=%s" % (key, value) for key, value in ses.cookies.get_dict().items() ])
                hasil = {"email":ff,"cookie":cok}
                return hasil



def auto():
        ses = requests.session()
        mail = choice(['catgroup.uk', 'goatmail.uk', 'sendnow.win', 'ccmail.uk', 'exdonuts.com', 'hamham.uk', 'digdig.org', 'owleyes.ch', 'stayhome.li', 'fanclub.pm', 'hotsoup.be', 'simaenaga.com', 'tapi.re', 'fuwari.be', 'magim.be', 'mirai.re', 'moimoi.re', 'heisei.be', 'honeys.be', 'mbox.re', 'uma3.be', 'instaddr.ch', 'quicksend.ch', 'instaddr.win', 'instaddr.uk', 'meruado.uk', 'nekosan.uk', 'niseko.be', 'kpost.be', 'wanko.be', 'mofu.be', 'usako.net', 'eay.jp', 'via.tokyo.jp', 'ichigo.me', 'choco.la', 'cream.pink', 'merry.pink', 'neko2.net', 'fuwamofu.com', 'ruru.be', 'macr2.com', 'f5.si', 'svk.jp'])
        ses.get("https://m.kuku.lu/index.php")
        user=""
        login2 = par(ses.get("https://m.kuku.lu/id.php").text,"html.parser")
        for c in login2.find_all("script"):
            if 'data: "action=addMailAddrByAuto' in str(c):
                ff=str(par(ses.get(f"https://m.kuku.lu/index.php?action=addMailAddrByManual&nopost=1&by_system=1&t={re.search('t=(.*?)&',str(c)).group(1)}&csrf_token_check={re.search('csrf_token_check=(.*?)&',str(c)).group(1)}&newdomain={mail}&newuser={user}&recaptcha_token=&").text,"html.parser")).replace("OK:","")
                cok = (";").join([ "%s=%s" % (key, value) for key, value in ses.cookies.get_dict().items() ])
                hasil={"email":ff,"cookie":cok}
                if not "@" in str(hasil):
                    hasil=auto()
                return hasil

def inbox(session,mail):
        try:mail=mail.split("@")[0]
        except:mail=None
        ses=requests.Session()
        ses.cookies.update({'cookie':session})
        log=par(ses.get("https://m.kuku.lu/recv.php").text,"html.parser")
        try:
            param = {"nopost":"1","csrf_token_check":re.search('csrf_token_check=(.*?)&',str(log)).group(1),"csrf_subtoken_check":re.search('csrf_subtoken_check=(.*?)"',str(log)).group(1)}
            maill = par(ses.get("https://m.kuku.lu/recv._ajax.php",params=param).text,"html.parser")
            res={}
            for g in maill.find_all("script"):                
                if "openMailData" in str(g):                    
                    if maill == None:
                            dat = re.search("openMailData(\(.*?)\)",str(g)).group(1).split("', '")
                            masuk = par(ses.post("https://m.kuku.lu/smphone.app.recv.view.php",data={"num":dat[0].replace("('",""),"key":dat[1],"noscroll":"1"}).text,"html.parser")                   
                            html=[]
                            for de in masuk.find_all('div'):
                                if len(de.text)>2:
                                    if '</script>' in str(de):pass
                                    else:
                                        if len(de.find_all('div'))>3:pass
                                        else:html.append(de)   
                            res.update({"text":str(re.sub(r'\s+', ' ', masuk.text)),"html":html})
                            break               
                    else:                        
                        if mail in str(g):
                            dat = re.search("openMailData(\(.*?)\)",str(g)).group(1).split("', '")
                            masuk = par(ses.post("https://m.kuku.lu/smphone.app.recv.view.php",data={"num":dat[0].replace("('",""),"key":dat[1],"noscroll":"1"}).text,"html.parser")
                            html=[]
                            for de in masuk.find_all('div'):
                                if len(de.text)>2:
                                    if '</script>' in str(de):pass
                                    else:
                                        if len(de.find_all('div'))>3:pass
                                        else:html.append(de)
                            res.update({"text":str(re.sub(r'\s+', ' ', masuk.text)),"html":html})
                            break
            try:
                return res            
            except Exception:
                return e
        except Exception as e : return e



def outbox(prom,to,texs,cookie):
        ses = requests.Session()
        ses.cookies.update({"cookie":cookie})   
        login2 = par(ses.get("https://m.kuku.lu/id.php").text,"html.parser")
        for c in login2.find_all("script"):        
            if 'data: "action=addMailAddrByAuto' in str(c):
                logi2 = par(ses.get(f"https://m.kuku.lu/smphone.app.new.php?&passcodelock=off&t={re.search('t=(.*?)&',str(c)).group(1)}&version=4400").text,"html.parser")
                file = re.search('file_hash", "(.*?)"',str(logi2)).group(1)
                token = re.search('csrf_token_check=(.*?)&',str(logi2)).group(1)
                send = re.search('sendtemp_hash=(.*?)&',str(logi2)).group(1)
                head = {
'Host': 'm.kuku.lu', 
'content-length': '396', 
'accept': 'application/json, text/javascript, */*; q=0.01', 
'x-requested-with': 'XMLHttpRequest', 
'user-agent': 'Mozilla/5.0 (Linux; Android 9; SAMSUNG Build/IFTHS; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.196 Mobile Safari/537.36 AndroidMailNowNativeVer=4400;MailNowApp=4400;', 
'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 
'origin': 'https://m.kuku.lu', 
'sec-fetch-site': 'same-origin', 
'sec-fetch-mode': 'cors', 
'sec-fetch-dest': 'empty', 
'accept-encoding': 'gzip, deflate, br', 
'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'}
                data = {
    "action": "sendMail",
    "ajax": 1,
    "csrf_token_check": token,
    "sendmail_replymode": "",
    "sendmail_replynum": "",
    "sendtemp_hash": send,
    "sendmail_from": prom,
    "sendmail_from_radio": prom,
    "sendmail_to": to,
    "sendmail_subject": to,
    "sendmail_content": texs,
    "sendmail_content_add": "",
    "file_hash": file,
                }
                pos = ses.post("https://m.kuku.lu/smphone.app.new.php",data=data,headers=head).json()
                return pos