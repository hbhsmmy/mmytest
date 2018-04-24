# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
from base64 import b64encode
from models import Client
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

#maildict['encode'] = 'gb23312'
#maildict['files'] = ['1.txt', '2.txt']
#maildict['to'] = 'xxx@xxx.com'
#maildict['from'] = 'XXX@XXX.com'
#maildict['subject'] = 'xxx'
#maildict['smtpsvr'] = 'smtp.XXX.com'
#maildict['user'] = 'xxx'
#maildict['password'] = 'xxx'

def SendMailWithFile(maildict, content):
    encode = 'utf-8'
    #if maildict.has_key('encode'):
    #    encode = maildict['encode']

    msg = MIMEMultipart()
    if maildict.has_key('files'):
        filelist = maildict['files']
        for filename in filelist:
            pos = filename.rfind('/')
            if pos == -1:
                pos = filename.rfind('\\')
            if (pos == -1):
                pos = 0
            filesubname = filename[pos:]
            att = MIMEText(open(filename, 'rb').read(), 'base64', encode)
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="'+ filesubname + '"'
            msg.attach(att)

    #strTo = ';'.join(maildict['to'])
    #print strTo
    #msg['to'] = strTo
    msg['from'] = maildict['from']
    # msg['from'] = '=?%s?B?%s?=' % ('utf-8',b64encode(maildict['from']))
    # msg['subject'] = maildict['subject']
    # print type(msg['subject'])

    msg['subject'] = '=?%s?B?%s?=' % ('utf-8',b64encode(maildict['subject']))
    print msg['subject']

    #不被当作垃圾邮件的关键代码--Begin
    msg["X-Priority"] = '3'
    msg["X-MSMail-Priority"] = "Normal"
    msg["X-Mailer"] = "Microsoft Outlook Express 6.00.2900.2869"
    msg["X-MimeOLE"] = "Produced By Microsoft MimeOLE V6.00.2900.2869"
    msg["ReturnReceipt"] = "1"
    #不被当作垃圾邮件的关键代码--End

    text_msg = MIMEText(content.encode('utf-8'), _subtype='html', _charset='utf-8')
    msg.attach(text_msg)
    try:
        server = smtplib.SMTP()
        if maildict.has_key('smtpport'):
            server.connect(maildict['smtpsvr'], maildict['smtpport'])
        else:
            server.connect(maildict['smtpsvr'])
        server.starttls()
        server.login(maildict['user'], maildict['password'])
        for toAdd in maildict['to']:
            del msg['to']
            msg['to'] = toAdd
            print msg['to'], toAdd
            server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
        print 'send mail success'
        return True
    except Exception, e:
        print str(e)
        return False

def TestSendMail(report_name,report_chinese,mail_to):
    maildict = {}
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/reports');
    maildict['files'] = [REPORT_ROOT+'/'+report_name]
    #maildict['to'] = ['dhke@gyasset.com','zdong@gyasset.com']
    maildict['to'] = [mail_to]
    maildict['from'] = '高毅资产客户服务<crm@gyasset.com>'
    maildict['subject'] = report_chinese
    maildict['smtpsvr'] = 'smtp.partner.outlook.cn'
    maildict['smtpport'] = 587
    maildict['user'] = 'crm@gyasset.com'
    maildict['password'] = 'Gaoyi001'
    return SendMailWithFile(maildict, '您好！附件为'+maildict['subject']+'，请您查收。\n如有疑问，您可以通过以下方式联系我们：\n电话：0755-88693999  传真：0755-88693940\n邮箱：IRgroup@gyassetcom\n\n顺祝商祺！\n高毅资产管理合伙企业\n\n')

def sendinfomail(subject, content, mail_to):
    maildict = {}
    maildict['to'] = [mail_to]
    maildict['from'] = '高毅资产客户服务<crm@gyasset.com>'
    maildict['subject'] = subject
    maildict['smtpsvr'] = 'smtp.partner.outlook.cn'
    maildict['smtpport'] = 587
    maildict['user'] = 'crm@gyasset.com'
    maildict['password'] = 'Gaoyi001'
    result =  SendMailWithFile(maildict, content)
    return result

