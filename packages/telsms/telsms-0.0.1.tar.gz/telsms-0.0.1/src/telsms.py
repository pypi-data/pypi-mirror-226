# -*- coding: UTF-8 -*-
'''
from qcloudsms_py import SmsMultiSender
from qcloudsms_py.httpclient import HTTPError


# 短信应用SDK AppID
appid = 1400465438  # SDK AppID是1400开头
# 短信应用SDK AppKey
appkey = "d671eba35fb6a02c36f8fd3c02a5fb59"

# 需要发送短信的手机号码
phone_numbers = ["13360069862"]

# 短信模板ID，需要在短信应用中申请
template_id = 824653  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请

# 签名
sms_sign = "ficash"  # NOTE: 这里的签名"腾讯云"只是一个示例


def messageSender(params):

    msender = SmsMultiSender(appid, appkey)
    try:
        result = msender.send_with_param(86, phone_numbers,
            template_id, params, sign=sms_sign, extend="", ext="")   # 签名参数不允许为空串
    except Exception as e:
        print(e)

    print(result)
'''




#无法成功，需要第三代申请密码保护 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests
import json
import time
import urllib.request
import socket

from vchatsms import WWXRobot


from_addr='1053207823@qq.com'   #邮件发送账号
qqCode='uddfdsnjasdfshibehb'   #授权码（这个要填自己获取到的）
smtp_server='smtp.qq.com'#固定写死
smtp_port=465#固定端口



####my_ip = str(json.load(urllib.request.urlopen('http://jsonip.com'))['ip'])
#my_ip = str(json.load(urllib.request.urlopen('http://api.ipify.org/?format=json'))['ip'])
#print(my_ip)

my_host = socket.gethostname()
print(my_host)

####储储
dingding_url='https://oapi.dingtalk.com/robot/send?access_token=cd5376e612295ee4b32dfff39de3d429510c021070e7a69b51e31028230adffc'
wxKey='5e680cf2-e925-4ce0-968a-9470a7dfa5e8'     ####web3
if my_host == 'DESKTOP-FHICKK2' or False:  ####测试时True,,真实的时候设置成False
    ####东莞满通工业园
    dingding_url='https://oapi.dingtalk.com/robot/send?access_token=cf1738afe2e6e1f693b00776d75a0bd93f165cebfe1e12dc2458f51452a9fb6f'
    wxKey='f58fb391-b8f5-424d-ad88-c15d65fe09e4'   ###天河拍森


def lklmake(strsubin):
    try:
        #配置服务器
        stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
        stmp.login(from_addr,qqCode)
        to_addrs='15813137712@139.com'   #接收邮件账号

        #组装发送内容
        message = MIMEText('', 'plain', 'utf-8')   #发送的内容
        message['From'] = Header(from_addr, 'utf-8')   #发件人
        message['To'] = Header(to_addrs, 'utf-8')   #收件人
        subject = strsubin
        message['Subject'] = Header(subject, 'utf-8')  #邮件标题

        stmp.sendmail(from_addr, to_addrs, message.as_string())
    except Exception as e:
        print ('邮件发送失败--' + str(e))
    print ('邮件发送成功')

def tencentmake(strsubin):
    try:
        #配置服务器
        stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
        stmp.login(from_addr,qqCode)
        to_addrs='15813137712@139.com'   #接收邮件账号

        #组装发送内容
        message = MIMEText('', 'plain', 'utf-8')   #发送的内容
        message['From'] = Header(from_addr, 'utf-8')   #发件人
        message['To'] = Header(to_addrs, 'utf-8')   #收件人
        subject = strsubin
        message['Subject'] = Header(subject, 'utf-8')  #邮件标题
        
        stmp.sendmail(from_addr, to_addrs, message.as_string())
    except Exception as e:
        print ('邮件发送失败--' + str(e))
    print ('邮件发送成功')

def chuChumake(strsubin):
    try:
        headers={'Content-Type': 'application/json'}
        program={
            "msgtype": "text",
            "text": {"content": "{0}币本位：{1}".format( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),strsubin)},
            }
        f=requests.post(dingding_url,data=json.dumps(program),headers=headers)
    except Exception as e:
        print ('dingding发送失败--' + str(e))
    print ('dingding发送成功')

def futuCheck(futuPort=11111):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(8)
    try:
        s.connect(('localhost',futuPort))
        print('futu connected.')
    except Exception as e:
        print('请打开openFutu客户端,Port::{0}'.format(futuPort))
        raise e

def sinaData(pippi,minute=240,wantK=31):
    ####https://blog.csdn.net/weixin_39729262/article/details/110033772
    ####比如sz000001指的是平安银行，而sh000001则是上证指数；scale表示的是时间长度，以分钟为基本单位，输入240就表示下载日K线数据，60就是小时K线数据，貌似最短时间是5分钟，并没有提供分钟数据；datalen则是获取数据的条数，在日K线的时间长度了，datalen就是获取60天日K数据，当然也可以获取60小时K数据。
    halipot=''
    if  pippi[0] in ['5','6']:     
        halipot='sh{0}'.format(pippi)
    elif  pippi[0] in ['1','3','0']:    ####!!!注意有时候0开头的有可能是上证的指数!!!!所以获取指数一定要用不同的函数
        halipot='sz{0}'.format(pippi)
    links='http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?symbol={0}&scale={1}&ma=no&datalen={2}'.format(halipot,minute,wantK)
    histData = urllib.request.urlopen(links).read()
    #print(links)
    #print(histData)
    time.sleep(1)
    histData = str(histData).split('(')[1].split(')')[0]
    histData=json.loads(histData)
    ###print(histData)
    return histData

def send_dingdingtext(strsubin):
    try:
        ####https://oapi.dingtalk.com/robot/send?access_token=e17805522c502715b7b2acfc13c7ee917f090b4f1814994f2b63d3ac59d26917
        headers={'Content-Type': 'application/json'}
        program={
            "msgtype": "text",
            "text": {"content": "{0}:{1}::主机地址{2}".format( time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),strsubin,my_host)},
            }
            ###req = urllib.request.Request(url,headers=headers,data=fdata)
        ###f=urllib.request.Request(url,data=json.dumps(program),headers=headers)
        f=requests.post(dingding_url,data=json.dumps(program),headers=headers)
        ####print(f.read().decode("utf-8"))
        print ('dingding发送成功')
    except Exception as e:
        print ('dingding发送失败--' + str(e))


def chuChumakexianhuo(strsubin):
    if my_host == 'DESKTOP-FHICKK2':
        print ('绕过dingding文字发送')
        ###send_dingdingtext(strsubin)
    else:
        print ('绕过dingding文字发送')
        ###send_dingdingtext(strsubin)


def tupianSend(strsubin,who=''):
    here_url=dingding_url
    if who=='ashare':
        here_url='https://oapi.dingtalk.com/robot/send?access_token=761aa3d60ca2bfce00b859caa2f25544490dd82e3e61d697292a4fdf4ee0e10a'
    if my_host == '55DESKTOP-FHICKK2':
        print ('绕过dingding发送')
    else:
        try:
            ####https://oapi.dingtalk.com/robot/send?access_token=e17805522c502715b7b2acfc13c7ee917f090b4f1814994f2b63d3ac59d26917
            ##'https://oapi.dingtalk.com/robot/send?access_token=e17805522c502715b7b2acfc13c7ee917f090b4f1814994f2b63d3ac59d26917'
            headers={'Content-Type': 'application/json'}
            program={
                'msgtype': 'markdown',
                "markdown": {
            "title": "图片消息",
            "text":  "![avatar]({0})".format(strsubin)
            ###"text":  "![avatar]({0}) ".format(baseStr)
            
                },
                }
                ###req = urllib.request.Request(url,headers=headers,data=fdata)
            ###f=urllib.request.Request(url,data=json.dumps(program),headers=headers)
            f=requests.post(here_url,data=json.dumps(program),headers=headers)
            ####print(f.read().decode("utf-8"))
            print ('dingding发送成功')
        except Exception as e:
            print ('dingding发送失败--' + str(e))

def fileSend(strsubin,fileN='表格',who=''):
    here_url=dingding_url
    if who=='ashare':
        here_url='https://oapi.dingtalk.com/robot/send?access_token=761aa3d60ca2bfce00b859caa2f25544490dd82e3e61d697292a4fdf4ee0e10a'
    if my_host == '55DESKTOP-FHICKK2':
        print ('绕过dingding发送')
    else:
        try:
            headers={'Content-Type': 'application/json'}
            program={
                'msgtype': 'file',
                "file": {
                        "mediaId":"{0}".format(strsubin),
                        "fileName":"{0}.xlsx".format(fileN),
                        "fileType":"xlsx",
            
                },
                }
            f=requests.post(here_url,data=json.dumps(program),headers=headers)
            ####print(f.read().decode("utf-8"))
            print ('dingding发送成功')
        except Exception as e:
            print ('dingding发送失败--' + str(e))


   
def vchatSendImage(imgfile,who=''):
    ###https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=5033827c-492f-4a9d-a1ac-581d73bce8f6
    here_key=wxKey
    if who=='ashare':
        here_key='5033827c-492f-4a9d-a1ac-581d73bce8f6'
    wwxrbt = WWXRobot(key=here_key)
    wwxrbt.send_image(local_file=imgfile)


if __name__ == '__main__':
    ##lklmake('nihao')
    ##readBase64('./output/202302核心长坡股票和etf_1day.png')
    ##fileSend('@lAzPDetfc5sXxknOW3LAxc5ueC4J')
    ##tupianSend('@lAzPDetfc5sXxknOW3LAxc5ueC4J',who='ashare')
    ##print(sinaData('000001',minute=60,wantK=10000))
    vchatSendImage('./output/AshareETF_futuData_1day_picture.png')
    ##ashare##https://oapi.dingtalk.com/robot/send?access_token=761aa3d60ca2bfce00b859caa2f25544490dd82e3e61d697292a4fdf4ee0e10a
    ####https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f58fb391-b8f5-424d-ad88-c15d65fe09e4










####新浪实时数据
#####新浪,,腾讯,,香港  数据  https://github.com/shidenggui/easyquotation

###http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?symbol=sh000001&scale=240&ma=no&datalen=31
'''
links = 'http://hq.sinajs.cn/list=' + codesrealTimeData = urllib.request.urlopen(links).read()realTimeData = realTimeData.decode('gbk').replace('"','').split('\n')data = {}for i in range(len(realTimeData)-1):    if len(realTimeData[i]) > 0:       data[realTimeData[i].split('=')[0].split('_')[2][2:]] = realTimeData[i].split('=')[1].split(',')[:-1]return data
'''

'''
def sinaData(pippi):
    import urllib.request
    links = 'http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?symbol=' + code + '&scale=' + str(scale) + '&ma=no&datalen='+str(datalen)
    histData = urllib.request.urlopen(links).read()
    histData = str(histData).split('[')[1]
    histData = histData[1:len(histData) - 4].split('},{')
    datas = []
    for i in range(0, len(histData)):    
        column = {}    
        dayData = histData[i].split(',')    
        for j in range(0, len(dayData)):       
            field = dayData[j].split(':"')       
            if field[0] == 'day':          
                column['date'] = field[1].replace('"', '')       
            else:          
                column[field[0]] = field[1].replace('"', '')    
                datas.append(column)
    return datas


'''