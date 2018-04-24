# -*- coding: utf-8 -*-
__author__ = 'zhangchengyiming'
from models import Investor,Inquiry,Article,Message,Job,Customer,recommendedFund,Client,Accredited,AccreditedDoc,Document,UserInfo
from django.shortcuts import render
import tasvr_pb2 as tasver
import os
import json
import pbjson
import requests
from django.http import JsonResponse
import hashlib
import time
from sendmail2 import TestSendMail

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('msyh', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gaoyicrm/static/fonts/msyh.ttf')))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph,Table,TableStyle,CellStyle

#url = 'http://115.159.154.36:10000'
url = 'http://127.0.0.1:10000'

def get_time():
    return time.strftime('%Y-%m-%d', time.localtime())

def get_time_details():
    return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())

def hashed_password(password=None):
    return hashlib.md5(password).hexdigest()

def checkDegree(request):
    investor = Investor.objects.get(id = request.session['userID'])
    if investor.password == hashed_password(request.POST['password']):
        content = {'is_exist':1}
    else:
        content = {'is_exist':0}
    return JsonResponse(content)

def checkPassword(request):
    investor = Investor.objects.get(id = request.session['userID'])
    if investor.password == hashed_password(request.POST['password']):
        content = {'is_exist':1}
    else:
        content = {'is_exist':0}
    return JsonResponse(content)

def modifyPhone1(request):
    investor = Investor.objects.get(id = request.session['userID'])
    if investor.mobile == request.POST['oldPhone'] and investor.password == hashed_password(request.POST['password']) and investor.idno == request.POST['cardCode']:
        content = {'success':1}
    else:
        content = {'success':0}
    return JsonResponse(content)

def modifyPhone2(request):
    investor = Investor.objects.get(id = request.session['userID'])
    investor.mobile = request.GET['phone']
    investor.save()
    return JsonResponse({})

def modifyOccupation(request):
    investor = Investor.objects.get(id = request.session['userID'])
    investor.education = request.GET['education']
    investor.occupation = request.GET['occupation']
    investor.save()
    return JsonResponse({})

def modifyAddress(request):
    province = request.GET['province']
    city = request.GET['city']
    details = request.GET['details']
    address = province + city + details
    investor = Investor.objects.get(id = request.session['userID'])
    investor.address = address
    investor.save()
    return JsonResponse({})

def account_modifyOccupation(request):
    return render(request,'account_modifyOccupation.html')

def account_modifyEmail(request):
    return render(request,'account_modifyEmail.html')

def account_modifyAddress(request):
    return render(request,'account_modifyAddress.html')

def account_modifyPhone(request):
    return render(request,'account_modifyPhone.html')

def account_modifyPassword(request):
    return render(request,'account_modifyPassword.html')

def finishOrNot(request):
    investor = Investor.objects.get(id = request.session['userID'])
    if investor.point == '_':
        content = {'finishOrNot':0}
    else:
        content = {'finishOrNot':1}
    return JsonResponse(content)

def bangding(request):
    return render(request,'bangding.html')

def notfound(request):
    return render(request,'404.html')

def weixininfo(request):
    result = requests.get(request.GET['weixinUrl'])
    resultJson = result.json()
    openid = resultJson['openid']
    print openid

    userInfoUrl = 'https://api.weixin.qq.com/sns/userinfo?access_token='+resultJson['access_token']+'&openid='+resultJson['openid']
    userInfoResult = requests.get(userInfoUrl)
    userInfoResultJson = userInfoResult.json()
    content = {'usernickname':userInfoResultJson['nickname'],'headimgurl':userInfoResultJson['headimgurl']}

    if Investor.objects.filter(openid = openid).exists():
        investor = Investor.objects.get(openid = openid)
        request.session['userID'] = investor.id
        content.update({'success':0})
    else:
        ta = tasver.WechatIdCheckReq()
        ta.wechatid = resultJson['openid']
        # ta.wechatid = 'o3zFCuLQfGhhwdaenalaIr8R9aQs'
        header = tasver.Header()
        header.cmd = 109
        header.ver = 0
        header.platform = 3
        header.content = pbjson.pb2json(ta)
        headdata = pbjson.pb2json(header)

        headers = {'content-type': 'application/json'}
        r = requests.post(url,headdata,headers=headers)
        headerRes = tasver.WebRspHeader()
        headerRes.ParseFromString(r.content)
        if headerRes.errCode == 0 :
            oAccountRsp = tasver.WechatIdCheckRsp()
            oAccountRsp.ParseFromString(headerRes.content)
            oAccountJon = pbjson.pb2json(oAccountRsp)
            if json.loads(oAccountJon)['investorid'] == '':
                request.session['openid'] = openid
            else:
                request.session['openid'] = json.loads(oAccountJon)['investorid']
            content.update({'success':1})
            # print json.loads(oAccountJon)
        else :
            print "ErrCode:"
            print headerRes.errCode
            print "ErrMsg:"
            # print headerRes.errMsg.encode("utf-8")

    return JsonResponse(content)

#填充问卷调查结果
def result(request):
    # print request.session['totalPoint']
    return JsonResponse({'totalPoint':request.session['totalPoint']})

def emailAuthentication(request):
    try:
        investor = Investor.objects.get(id = request.session['userID'])
        investor.email = request.GET['email']
        investor.save()
        contact = {'type':'success'}
    except:
        contact = {'type':'fail'}
    return JsonResponse(contact)

def get_bespeak(request):
    investor = Investor.objects.get(id = request.session['userID'])
    content = {'fundName':request.session['choosedFund'],'mobile':investor.mobile}
    return JsonResponse(content)


#返回月报
def report(request):
    oAccountRsp = report_create(request)
    return JsonResponse({'url':'../static/reports/'+(oAccountRsp.reportname).encode('utf-8')})

def sendmail(request):
    oAccountRsp = report_create(request)
    if TestSendMail(oAccountRsp.reportname,oAccountRsp.chinesename,request.GET['email_to']):
        return JsonResponse({'success':200})
    else:
        return JsonResponse({'success':403})

def report_create(request):
    ta = tasver.FundReportReq()
    ta.reportid = int(request.GET['reportid'])
    header = tasver.Header()
    header.cmd = 108
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.FundReportRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/reports')
        WriteFileData = open(REPORT_ROOT+'/'+(oAccountRsp.reportname).encode('utf-8'),'wb')
        WriteFileData.write(oAccountRsp.content)
        WriteFileData.close()
        # 修复基金报告导出问题
        # print oAccountRsp
        return oAccountRsp
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def creatNewPDF(client, clientSubArray, clientArray, pointList):
    story=[]
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']


    rpt_title = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">风险属性评估问卷(自然人适用) </font></b><br/><br/><br/></para>'
    story.append(Paragraph(rpt_title,normalStyle))

    clientName = client.customer_name
    if int(client.id_type) == 0:
        cardType = '身份证'
    elif int(client.id_type) == 1:
        cardType = '护照'
    elif int(client.id_type) == 2:
        cardType = '军官证'
    elif int(client.id_type) == 3:
        cardType = '士兵证'
    elif int(client.id_type) == 4:
        cardType = '港澳居民来往内地通行'
    elif int(client.id_type) == 5:
        cardType = '户口本'
    elif int(client.id_type) == 6:
        cardType = '外国护照'
    elif int(client.id_type) == 7:
        cardType = '其他'
    elif int(client.id_type) == 8:
        cardType = '文职证'
    elif int(client.id_type) == 9:
        cardType = '警官证'
    else:
        cardType = '台胞证'
    cardNumber = client.id_no
    currDate = time.strftime("%Y-%m-%d", time.localtime())

    text = '''<para leading=18 fontSize=10 align=center><font face="msyh">投资者姓名：%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;填写日期：%s</font><br/><br/><br/></para>'''%('<u>__'+clientName+'__</u>','<u>__'+currDate+'__</u>')
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=10 align=left><font face="msyh"><b>风险提示：私募基金投资需承担各类风险，本金可能遭受损失。同时，私募基金投资还要考虑市场风险、信用风险、流动性风险、操作风险等各类投资风险。您在基金认购过程中应当注意核对自己的风险识别和风险承受能力，选择与自己风险识别能力和风险承受能力相匹配的私募基金。</b></font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><font face="msyh"><b>一、关于这份问卷：</b></font><br/><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本问卷旨在协助您了解自己对投资风险的承受度和投资目标，问卷信息将帮助我们提供适合您的投资产品供您参考。</font><br/>
              <font face="msyh">以下一系列问题可在您选择合适的私募基金前，协助评估您的风险承受能力、理财方式及投资目标：</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.您是否为自己购买私募基金产品：&nbsp;&nbsp;&nbsp;'''+clientSubArray[0]+'''&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'''+clientSubArray[1]+'''</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.您符合以下何种合格投资者财务条件：</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'''+clientSubArray[2]+'''</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'''+clientSubArray[3]+'''</font><br/><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;投资人签字确认：______________________</font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><font face="msyh"><b>二、问卷题目（单选题）：</b></font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    for i in range(0,len(clientArray)):
        if i == 5 or i == 11 or i == 16 or i == 21 or i == 25 or i == 30 or i == 36 or i == 41 or i == 46 or i == 51 or i == 56 or i == 61:
            text = '<para leading=18 fontSize=9 align=left><font face="msyh">'+clientArray[i]+'</font><br/><br/></para>'
        else:
            text = '<para leading=18 fontSize=9 align=left><font face="msyh">'+clientArray[i]+'</font><br/></para>'
        story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><b><font face="msyh">三、测试结果：</font></b><br/><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;风险承受能力从低到高分为C1（含风险承受能力最低类别）、C2、C3、C4、C5五种类型。分类标准如下表所示:</font><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    component_data= [['风险承受能力','评估问卷得分'],
                     ['C1','32分及以下'],
                     ['C2','33～38分'],
                     ['C3','39～43分'],
                     ['C4','44～48分'],
                     ['C5','49分及以上']]

    cellStyleSheetCenter = CellStyle(name = 'sheet')
    cellStyleSheetCenter.alignment = 'CENTER'
    cellStyleSheetCenter.valign = 'MIDDLE'
    cellStyleSheetCenter.fontsize = 10
    cellStyleSheetLEFT = CellStyle(name = 'sheet')
    cellStyleSheetLEFT.alignment = 'LEFT'
    cellStyleSheetLEFT.fontsize = 10
    cellStyleSheetLEFT.valign = 'TOP'
    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter]]

    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[150,150],rowHeights=[20,20,20,20,20,20])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    totalPoint = 0
    for point in (pointList).split('.'):
        totalPoint += int(point)

    if totalPoint <= 32:
        level = 1
    elif totalPoint <= 38:
        level = 2
    elif totalPoint <= 43:
        level = 3
    elif totalPoint <= 48:
        level = 4
    else:
        level = 5

    if int(pointList.split('.')[11]) == 1:
        level = 1

    text = '''<para leading=18 fontSize=10 align=left><br/><font face="msyh">您的测试得分为&nbsp;&nbsp;%s&nbsp;&nbsp;分</font><font face="msyh">风险承受能力为C&nbsp;&nbsp;%s&nbsp;&nbsp;等级。</font><br/><br/><br/><br/></para>'''%('<u>__'+str(totalPoint)+'__</u>','<u>__'+str(level)+'__</u>')
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><font face="msyh"><b>四、风险程度确认：</b></font><br/><br/><font face="msyh">根据基金产品风险等级名录（见尾页），本基金风险评级为R3，仅适合具有<u>C3及以上</u>风险识别能力和风险承受<br/>能力的投资者认购/申购。</font><br/><br/>
              <font face="msyh">如果您的测试结果属于上述类型，决定认购此基金产品，请签字确认：<u>本人已经如实填写本《风险属性评估问卷》，充分了解了自己的风险承受类型和适合购买的产品类型，并愿意承担相关风险。</u></font><br/><br/><br/>
              <font face="msyh">投资者签名：___________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日期：___________________</font><br/><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><b><font face="msyh">五、投资者风险匹配告知书及投资者确认函</font></b><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))


    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetCenter],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetCenter,cellStyleSheetCenter],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetCenter,cellStyleSheetCenter]]

    component_data= [['投资者风险匹配告知书及投资者确认函','','',''],
                     ['投资者姓名/名称',clientName,'',''],
                     ['证件类型',cardType,'证件编号',cardNumber]]

    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[100,80,80,140],rowHeights=[20,20,20])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('SPAN',(0,0),(3,0)),                    #合并第一行
    ('SPAN',(1,1),(3,1)),                    #合并第二行
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT]]

    component_data= [[Paragraph('<para fontSize=9 align=center><font face="msyh">投资者风险匹配</font><br/><font face="msyh">告知书</font></para>',normalStyle),Paragraph('<para leading=16 fontSize=9 align=left><font face="msyh" fontsize=9>尊敬的投资者：<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;根据您/贵机构填写的《投资者基本信息表》，依据相关法律、法规的规定，我司将您认定为专业投资者/普通投资者。结合您/贵机构填写的《风险测评问卷》以及其它相关信息，我司对您的风险承受能力进行了综合评估，现得到评估结果如下： <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;您/贵机构的风险承受能力为：C'+'<u>__'+str(level)+'__</u>'+'，依据我司的投资者与产品、服务风险等级匹配规则，您/贵机构的风险承受能力等级与我司（产品、服务风险等级）相匹配。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我司在此郑重提醒，我司向您/贵机构销售的产品或提供的服务将以您的风险承受能力等级和投资品种、期限为基础，若您/贵机构提供的信息发生任何重大变化，您/贵机构应当及时以书面方式通知我司。我司建议您/贵机构审慎评判自身风险承受能力、结合资深投资行为，认真填写投资品种、期限，并做出审慎的投资判断。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如同意我司评估结果，请在投资者确认函中签字，以示同意。<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;销售人员签字：<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;销售机构签章：<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日</font></para>',normalStyle),'','','',''],
                     [Paragraph('<para fontSize=9 align=center><font face="msyh">投资者确认函</font></para>',normalStyle),Paragraph('<para leading=16 fontSize=9 align=left><font face="msyh" fontsize=9>尊敬的（销售机构）：<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人/本机构已仔细阅读贵司的《投资者类型及风险匹配告知书》，已充分知晓并理解贵司对本人/本机构的风险承受能力评估及产品、服务风险等级匹配结果。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人/本机构对该《投资者类型及风险匹配告知书》内容没有异议，愿意遵守法律、法规及贵司有关规定，通过贵司购买产品或者服务。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人/本机构承诺，将及时以书面方式如实地向贵司告知本人/本机构的重大信息变更。 本确认函系本人/本机构独立、自主、真实的意思表示。<br/>特此确认。<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;投资者签字/盖章<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日<br/><br/></font></para>',normalStyle),'','','',''],
                     ['',Paragraph('<para fontSize=9 align=center><font face="msyh">授权经办人</font><br/><font face="msyh">信息</font></para>',normalStyle),'经办人','','职务',''],
                     ['','','证件类型','','证件号码',''],
                     ['','',Paragraph('<para leading=12 fontSize=9 align=left><font face="msyh" fontsize=9><br/>经办人签字：<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日</font></para>',normalStyle),'','','']]
    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[80, 60, 55, 75, 55, 75],rowHeights=[330,230,20,20,60])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('SPAN',(1,0),(5,0)),                    #合并第一行
    ('SPAN',(1,1),(5,1)),
    ('SPAN',(0,1),(0,4)),
    ('SPAN',(1,2),(1,4)),
    ('SPAN',(2,4),(5,4)),
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    text = '''<br/><br/>'''
    story.append(Paragraph(text,normalStyle))


    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetCenter],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT]]

    component_data= [['附表1：基金产品或者服务风险等级划分参考标准',''],
                     ['风险等级','产品参考因素'],
                     ['R1',Paragraph('<font face="msyh" fontsize=9>产品结构简单，过往业绩及净值的历史波动率低，投资标的流动性很好、不含衍生品，估值政策清晰，杠杆不超监管部门规定的标准。</font>',normalStyle)],
                     ['R2',Paragraph('<font face="msyh" fontsize=9>产品结构简单，过往业绩及净值的历史波动率较低，投资标的流动性好、投资衍生品以套期保值为目的，估值政策清晰，杠杆不超监管部门规定的标准。</font>',normalStyle)],
                     ['R3',Paragraph('<font face="msyh" fontsize=9>产品结构较简单，过往业绩及净值的历史波动率较高，投资标的流动性较好、投资衍生品以对冲为目的，估值政策清晰，杠杆不超监管部门规定的标准。</font>',normalStyle)],
                     ['R4',Paragraph('<font face="msyh" fontsize=9>产品结构较复杂，过往业绩及净值的历史波动率高，投资标的流动性较差，估值政策较清晰，一倍(不含)以上至三倍(不含)以下杠杆。</font>',normalStyle)],
                     ['R5',Paragraph('<font face="msyh" fontsize=9>产品结构复杂，过往业绩及净值的历史波动率很高，投资标的流动性差，估值政策不清晰，三倍（含）以上杠杆。</font>',normalStyle)],
                     [Paragraph('<font face="msyh" fontsize=9>注：1、上述风险划分标准为参考因素，基金募集机构可以根据实际情况，确定评估因素和各项因素的分值和权重，建立评估分值与具体产品风险等级的对应关系，基金服务的风险等级应按照服务涵盖的产品组合的风险等级划分。</font>',normalStyle),''],
                     [Paragraph('<font face="msyh" fontsize=9>2、基金服务指以销售基金产品为目的开展的基金推介、基金组合投资建议等活动。</font>',normalStyle),''],
                     [Paragraph('<font face="msyh" fontsize=9>3、产品或服务的风险等级至少为五级，风险等级名称可以结合实际情况进行调整。</font>',normalStyle),''],
                     [Paragraph('<font face="msyh" fontsize=9>4、R4、R5杠杆水平是指无监管部门明确规定的产品杠杆水平。</font>',normalStyle),'']]
    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[200,200],rowHeights=[20,20,50,55,55,50,50,45,20,20,20])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('SPAN',(0,0),(1,0)),#合并第一行前两列
    ('SPAN',(0,7),(1,7)),#合并第八行前两列
    ('SPAN',(0,8),(1,8)),#合并第九行前两列
    ('SPAN',(0,9),(1,9)),#合并第十行前两列
    ('SPAN',(0,10),(1,10)),#合并第十一行前两列
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    text = '''<para leading=18 fontSize=9 align=left><b><font face="msyh"><br/><br/>重要声明：</font></b><br/><font face="msyh">本风险属性评估问卷结果是根据被调查人填写问卷时所提供的机构客户资料而推论得出，其结果将作为被调查人投资本机构基金产品的参考资料。此问卷内容及结果不构成与被调查人的要约，上海高毅资产管理合伙企业（有限合伙）将不对此问卷的准确性及信息是否完整负责。上海高毅资产管理合伙企业（有限合伙）明确规定所有获准使用此资料的员工均须遵守公司的保密责任。</font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    timeTampName = str(time.time())+'.pdf'
    doc = SimpleDocTemplate(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gaoyicrm/static/tempfiles/'+ timeTampName))
    doc.build(story)
    return timeTampName

def createOrgPDF(client, clientArray, pointList):
    story=[]
    stylesheet=getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    rpt_title = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">风险属性评估问卷(机构适用) </font></b><br/><br/><br/></para>'
    story.append(Paragraph(rpt_title,normalStyle))

    clientName = client.customer_name
    cardType = client.id_type
    cardNumber = client.id_no
    currDate = time.strftime("%Y-%m-%d", time.localtime())

    text = '''<para leading=18 fontSize=10 align=center><font face="msyh">投资者名称：%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;填写日期：%s</font><br/><br/><br/></para>'''%('<u>__'+clientName+'__</u>','<u>__'+currDate+'__</u>')
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=10 align=left><font face="msyh"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本问卷旨在了解贵单位可承受的风险程度等情况，借此协助贵单位选择合适的金融产品或金融服务类别，以符合贵单位的风险承受能力。</b></font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;风险承受能力评估是本公司向客户履行适当性职责的一个环节，其目的是使本公司所提供的金融产品或金融服务与贵单位的风险承受能力等级相匹配。</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本公司特别提醒贵单位：本公司向客户履行风险承受能力评估等适当性职责，并不能取代贵单位自己的投资判断，也不会降低金融产品或金融服务的固有风险。同时，与金融产品或金融服务相关的投资风险、履约责任以及费用等将由贵单位自行承担。</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本公司提示贵单位：本公司根据贵单位提供的信息对贵单位进行风险承受能力评估，开展适当性工作。贵单位应当如实提供相关信息及证明材料，并对所提供的信息和证明材料的真实性、准确性、完整性负责。</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本公司建议：当贵单位的各项状况发生重大变化时，需对贵单位所投资的金融产品及时进重新审视，以确保贵单位的投资决定与贵单位可承受的投资风险程度等实际情况一致。</font><br/>
              <font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本公司在此承诺，对于贵单位在本问卷中所提供的一切信息，本公司将严格按照法律要求承担保密义务。除法律法规规定的有权机关依法定程序进行查询以外，本公司保证不会将涉及贵单位的任何信息提供、泄露给任何第三方，或者将相关信息用于违法、不当用途。</font><br/><br/></para>'''

    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><font face="msyh"><b>一、问卷题目：</b></font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    for i in range(0,len(clientArray)):
        if i == 4 or i == 9 or i == 14 or i == 19 or i == 25 or i == 30 or i == 35 or i == 39 or i == 44 or i == 49 or i == 60 or i == 54 or i == 66 or i == 70 or i ==75 or i == 81 or i == 86 or i == 92 or i == 97:
            text = '<para leading=18 fontSize=9 align=left><font face="msyh">'+clientArray[i]+'</font><br/><br/></para>'
        else:
            text = '<para leading=18 fontSize=9 align=left><font face="msyh">'+clientArray[i]+'</font><br/></para>'
        story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><b><font face="msyh">二、测试结果：</font></b><br/><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;风险承受能力从低到高分为C1（含风险承受能力最低类别）、C2、C3、C4、C5五种类型。分类标准如下表所示:</font><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    component_data= [['风险承受能力','评估问卷得分'],
                     ['C1','58分及以下'],
                     ['C2','59～67分'],
                     ['C3','68～76分'],
                     ['C4','77～85分'],
                     ['C5','86分及以上']]

    cellStyleSheetCenter = CellStyle(name = 'sheet')
    cellStyleSheetCenter.alignment = 'CENTER'
    cellStyleSheetCenter.valign = 'MIDDLE'
    cellStyleSheetCenter.fontsize = 10
    cellStyleSheetLEFT = CellStyle(name = 'sheet')
    cellStyleSheetLEFT.alignment = 'LEFT'
    cellStyleSheetLEFT.fontsize = 10
    cellStyleSheetLEFT.valign = 'TOP'
    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter],
                 [cellStyleSheetCenter,cellStyleSheetCenter]]

    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[150,150],rowHeights=[20,20,20,20,20,20])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    totalPoint = 0
    for point in (pointList).split('.'):
        totalPoint += int(point)

    if totalPoint <= 58:
        level = 1
    elif totalPoint <= 67:
        level = 2
    elif totalPoint <= 76:
        level = 3
    elif totalPoint <= 85:
        level = 4
    else:
        level = 5

    if int((pointList).split('.')[16]) == 1:
        level = 1

    text = '''<para leading=18 fontSize=10 align=left><br/><font face="msyh">您的测试得分为&nbsp;&nbsp;%s&nbsp;&nbsp;分</font><font face="msyh">风险承受能力为C&nbsp;&nbsp;%s&nbsp;&nbsp;等级。</font><br/></para>'''%('<u>__'+str(totalPoint)+'__</u>','<u>__'+str(level)+'__</u>')
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><br/><b><font face="msyh">三、风险程度确认：</font></b><br/>
              <font face="msyh">根据基金产品风险等级名录（见尾页），本基金风险评级为R3，仅适合具有<u>C3及以上</u>风险识别能力和风险承受</font><br/>
              <font face="msyh">能力的投资者认购/申购。</font><br/>
              <font face="msyh">如果贵公司的测试结果属于上述类型，决定认购此基金产品，请签字确认：<u>本公司已经如实填写本《风险属性评估问卷》，充分了解了自己的风险承受类型和适合购买的产品类型，并愿意承担相关风险。在此郑重承诺以上填写的内容真实、准确、完整。若本机构提供的信息发生任何重大变化，本机构将及时书面通知贵公司。</u></font><br/><br/>
              <font face="msyh">投资者签名：___________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日期：___________________</font><br/><br/>
              <font face="msyh">投资者盖章：___________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日期：___________________</font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    text = '''<para leading=18 fontSize=9 align=left><b><font face="msyh">四、投资者风险匹配告知书及投资者确认函</font></b><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    if int(client.id_type) == 0:
        cardType = '组织机构代码证'
    elif int(client.id_type) == 1:
        cardType = '营业执照'
    elif int(client.id_type) == 2:
        cardType = '行政机关'
    elif int(client.id_type) == 3:
        cardType = '社会团体'
    elif int(client.id_type) == 4:
        cardType = '军队'
    elif int(client.id_type) == 5:
        cardType = '武警'
    elif int(client.id_type) == 6:
        cardType = '下属机构'
    elif int(client.id_type) == 7:
        cardType = '基金会'
    elif int(client.id_type) == 8:
        cardType = '其他'
    elif int(client.id_type) == 9:
        cardType = '社会统一信用代码'
    elif int(client.id_type) == 12:
        cardType = '产品备案编码'

    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetCenter],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetCenter,cellStyleSheetCenter],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetCenter,cellStyleSheetCenter]]

    component_data= [['投资者风险匹配告知书及投资者确认函','','',''],
                     ['投资者姓名/名称',clientName,'',''],
                     ['证件类型',cardType,'证件编号',cardNumber]]

    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[80,110,70,140],rowHeights=[20,20,20])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('SPAN',(0,0),(3,0)),                    #合并第一行
    ('SPAN',(1,1),(3,1)),
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetCenter,cellStyleSheetCenter,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT,cellStyleSheetLEFT]]

    component_data= [[Paragraph('<para fontSize=9 align=center><font face="msyh">投资者风险匹配</font><br/><font face="msyh">告知书</font></para>',normalStyle),Paragraph('<para leading=16 fontSize=9 align=left><font face="msyh" fontsize=9>尊敬的投资者：<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;根据您/贵机构填写的《投资者基本信息表》，依据相关法律、法规的规定，我司将您认定为专业投资者/普通投资者。结合您/贵机构填写的《风险测评问卷》以及其它相关信息，我司对您的风险承受能力进行了综合评估，现得到评估结果如下： <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;您/贵机构的风险承受能力为：C'+'<u>__'+str(level)+'__</u>'+'，依据我司的投资者与产品、服务风险等级匹配规则，您/贵机构的风险承受能力等级与我司（产品、服务风险等级）相匹配。<br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;我司在此郑重提醒，我司向您/贵机构销售的产品或提供的服务将以您的风险承受能力等级和投资品种、期限为基础，若您/贵机构提供的信息发生任何重大变化，您/贵机构应当及时以书面方式通知我司。我司建议您/贵机构审慎评判自身风险承受能力、结合资深投资行为，认真填写投资品种、期限，并做出审慎的投资判断。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;如同意我司评估结果，请在投资者确认函中签字，以示同意。<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;销售人员签字：<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;销售机构签章：<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日</font></para>',normalStyle),'','','',''],
                     [Paragraph('<para fontSize=9 align=center><font face="msyh">投资者确认函</font></para>',normalStyle),Paragraph('<para leading=16 fontSize=9 align=left><font face="msyh" fontsize=9>尊敬的（销售机构）：<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人/本机构已仔细阅读贵司的《投资者类型及风险匹配告知书》，已充分知晓并理解贵司对本人/本机构的风险承受能力评估及产品、服务风险等级匹配结果。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人/本机构对该《投资者类型及风险匹配告知书》内容没有异议，愿意遵守法律、法规及贵司有关规定，通过贵司购买产品或者服务。<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;本人/本机构承诺，将及时以书面方式如实地向贵司告知本人/本机构的重大信息变更。 本确认函系本人/本机构独立、自主、真实的意思表示。<br/>特此确认。<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;投资者签字/盖章<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日<br/><br/></font></para>',normalStyle),'','','',''],
                     ['',Paragraph('<para fontSize=9 align=center><font face="msyh">授权经办人</font><br/><font face="msyh">信息</font></para>',normalStyle),'经办人','','职务',''],
                     ['','','证件类型','','证件号码',''],
                     ['','',Paragraph('<para leading=12 fontSize=9 align=left><font face="msyh" fontsize=9><br/>经办人签字：<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;月&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日</font></para>',normalStyle),'','','']]
    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[80, 60, 55, 75, 55, 75],rowHeights=[330,230,20,20,60])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('SPAN',(1,0),(5,0)),                    #合并第一行
    ('SPAN',(1,1),(5,1)),
    ('SPAN',(0,1),(0,4)),
    ('SPAN',(1,2),(1,4)),
    ('SPAN',(2,4),(5,4)),
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    text = '''<br/><br/>'''
    story.append(Paragraph(text,normalStyle))


    cellStyleList = [[cellStyleSheetCenter,cellStyleSheetCenter],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT],
                     [cellStyleSheetLEFT,cellStyleSheetLEFT]]

    component_data= [['附表1：基金产品或者服务风险等级划分参考标准',''],
                     ['风险等级','产品参考因素'],
                     ['R1',Paragraph('<font face="msyh" fontsize=9>产品结构简单，过往业绩及净值的历史波动率低，投资标的流动性很好、不含衍生品，估值政策清晰，杠杆不超监管部门规定的标准。</font>',normalStyle)],
                     ['R2',Paragraph('<font face="msyh" fontsize=9>产品结构简单，过往业绩及净值的历史波动率较低，投资标的流动性好、投资衍生品以套期保值为目的，估值政策清晰，杠杆不超监管部门规定的标准。</font>',normalStyle)],
                     ['R3',Paragraph('<font face="msyh" fontsize=9>产品结构较简单，过往业绩及净值的历史波动率较高，投资标的流动性较好、投资衍生品以对冲为目的，估值政策清晰，杠杆不超监管部门规定的标准。</font>',normalStyle)],
                     ['R4',Paragraph('<font face="msyh" fontsize=9>产品结构较复杂，过往业绩及净值的历史波动率高，投资标的流动性较差，估值政策较清晰，一倍(不含)以上至三倍(不含)以下杠杆。</font>',normalStyle)],
                     ['R5',Paragraph('<font face="msyh" fontsize=9>产品结构复杂，过往业绩及净值的历史波动率很高，投资标的流动性差，估值政策不清晰，三倍（含）以上杠杆。</font>',normalStyle)],
                     [Paragraph('<font face="msyh" fontsize=9>注：1、上述风险划分标准为参考因素，基金募集机构可以根据实际情况，确定评估因素和各项因素的分值和权重，建立评估分值与具体产品风险等级的对应关系，基金服务的风险等级应按照服务涵盖的产品组合的风险等级划分。</font>',normalStyle),''],
                     [Paragraph('<font face="msyh" fontsize=9>2、基金服务指以销售基金产品为目的开展的基金推介、基金组合投资建议等活动。</font>',normalStyle),''],
                     [Paragraph('<font face="msyh" fontsize=9>3、产品或服务的风险等级至少为五级，风险等级名称可以结合实际情况进行调整。</font>',normalStyle),''],
                     [Paragraph('<font face="msyh" fontsize=9>4、R4、R5杠杆水平是指无监管部门明确规定的产品杠杆水平。</font>',normalStyle),'']]
    component_table = Table(component_data, cellStyles=cellStyleList, colWidths=[200,200],rowHeights=[20,20,50,55,55,50,50,45,20,20,20])
    component_table.setStyle(TableStyle([
    ('FONTNAME',(0,0),(-1,-1),'msyh'),       #字体
    ('SPAN',(0,0),(1,0)),#合并第一行前两列
    ('SPAN',(0,7),(1,7)),#合并第八行前两列
    ('SPAN',(0,8),(1,8)),#合并第九行前两列
    ('SPAN',(0,9),(1,9)),#合并第十行前两列
    ('SPAN',(0,10),(1,10)),#合并第十一行前两列
    ('GRID',(0,0),(-1,-1),0.5,colors.black), #设置表格框线为黑色，线宽为0.5
    ]))
    story.append(component_table)

    text = '''<para leading=18 fontSize=9 align=left><b><font face="msyh"><br/><br/>重要声明：</font></b><br/><font face="msyh">本风险属性评估问卷结果是根据被调查人填写问卷时所提供的机构客户资料而推论得出，其结果将作为被调查人投资本机构基金产品的参考资料。此问卷内容及结果不构成与被调查人的要约，上海高毅资产管理合伙企业（有限合伙）将不对此问卷的准确性及信息是否完整负责。上海高毅资产管理合伙企业（有限合伙）明确规定所有获准使用此资料的员工均须遵守公司的保密责任。</font><br/><br/></para>'''
    story.append(Paragraph(text,normalStyle))

    timeTampName = str(time.time())+'.pdf'
    doc = SimpleDocTemplate(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gaoyicrm/static/tempfiles/'+ timeTampName))
    doc.build(story)

    return timeTampName
