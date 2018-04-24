# -*- coding: utf-8 -*-
__author__ = 'zhangchengyiming'
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from models import Client
pdfmetrics.registerFont(TTFont('msyh', 'gaoyicrm/static/fonts/msyh.ttf'))
pdfmetrics.registerFont(TTFont('jczt', 'gaoyicrm/static/fonts/jczt.ttf'))
def DrawCanvasPerson1(c,clientID,date,qaArray):
    lineheight = 15
    client = Client.objects.get(client_id = clientID)
    c.setFont("jczt", 13)
    text = u'风险属性评估问卷(自然人适用)'
    c.drawString(3*inch,11*inch,text)
    begy = 11*inch - lineheight*2
    c.setFont("msyh", 10)
    text = u'投资者姓名：    '+client.customer_name+'            填写日期：    '+date+'    '
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'风险提示：私募基金投资需承担各类风险，本金可能遭受损失。同时，私募基金投资还要考虑市场风险、'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'信用风险、流动性风险、操作风险等各类投资风险。您在基金认购过程中应当注意核对自己的风险识别和'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'风险承受能力，选择与自己风险识别能力和风险承受能力相匹配的私募基金。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'一、关于这份问卷：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       本问卷旨在协助您了解自己对投资风险的承受度和投资目标，问卷信息将帮助我们提供适合您的投资'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'产品供您参考。'
    c.drawString(inch,begy,text)


    begy = begy - lineheight
    text = u'       以下一系列问题可在您选择合适的私募基金前，协助评估您的风险承受能力、理财方式及投资目标：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       1、您是否为自己购买私募基金产品：  a.是；   b.不是'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       2、您符合以下何种合格投资者财务条件：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       a.是；   b.不是'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       a．符合金融资产不低于300万元（金融资产包括银行存款、股票、债券、基金份额、资产管理计划、'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'银行理财产品、信托计划、保险产品、期货权益等）；'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       b. 符合最近三年个人年均收入不低于50万元；'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'       投资人签字确认：________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'二、投资人基本情况'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'       姓名：    '+client.customer_name+'           联系方式：'+client.customer_mobile+''
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    if client.id_no != '':
        if client.id_type == '0':
            text = u'       证件类型： 身份证       证件号码： '+client.id_no+''
        elif client.id_type == '1':
            text = u'       证件类型： 护照         证件号码： '+client.id_no+''
        elif client.id_type == '2':
            text = u'       证件类型： 军官证       证件号码： '+client.id_no+''
        elif client.id_type == '3':
            text = u'       证件类型： 士兵证       证件号码： '+client.id_no+''
        elif client.id_type == '4':
            text = u'       证件类型： 港澳居民来往内地通行      证件号码： '+client.id_no+''
        elif client.id_type == '5':
            text = u'       证件类型： 户口本       证件号码： '+client.id_no+''
        elif client.id_type == '6':
            text = u'       证件类型： 外国护照     证件号码： '+client.id_no+''
        elif client.id_type == '7':
            text = u'       证件类型： 其他         证件号码： '+client.id_no+''
        elif client.id_type == '8':
            text = u'       证件类型： 文职证       证件号码： '+client.id_no+''
        elif client.id_type == '9':
            text = u'       证件类型： 警官证       证件号码： '+client.id_no+''
        elif client.id_type == 'A':
            text = u'       证件类型： 台胞证       证件号码： '+client.id_no+''
    else:
        text = u'       证件类型：________________      证件号码：________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'三、问卷题目'
    c.drawString(inch,begy,text)
    count = 0
    for line in qaArray:
        if count == 0 or count%5 == 0:
            begy = begy - lineheight*2
        else:
            begy = begy - lineheight*1
        c.drawString(inch,begy,line)
        count = count + 1

def DrawCanvasPerson2(c,qaArray):
    c.setFont("msyh", 10)
    lineheight = 15
    begy = 11.5*inch
    count = 0
    for line in qaArray:
        if len(line)>48:
            line1 = line[0:48]
            line2 = line[48:]
            begy = begy - lineheight*2
            c.drawString(inch,begy,line1)
            begy = begy - lineheight*1
            c.drawString(inch,begy,line2)
            count = count + 1
            continue
        if count == 0 or count%5 == 0:
            if count == 40:
                begy = begy - lineheight*1
            else:
                print count
                begy = begy - lineheight*2
        else:
            begy = begy - lineheight*1
        c.drawString(inch,begy,line)
        count = count + 1

def DrawCanvasPerson3(c,qaArray,totalPoint):
    c.setFont("msyh", 10)
    lineheight = 15
    begy = 11.5*inch
    count = 0
    for line in qaArray:
        if count == 0 or count%5 == 0:
            begy = begy - lineheight*2
        else:
            begy = begy - lineheight*1
        c.drawString(inch,begy,line)
        count = count + 1

    begy = begy - lineheight*2
    text = u'四、测试结果：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = '得分：  ' + str(totalPoint)
    if totalPoint < 33:
        text = text + '        类型：保守型'
    elif totalPoint <= 46:
        text = text + '        类型：成长型'
    else:
        text = text + '        类型：进取型'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*2
    text = u'1、33分以下，属于保守型的投资者。可以考虑货币型等低风险产品，不适合风险程度较高的产品，考虑'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'到本基金产品“高风险、高收益”的特征，我们不建议您考虑本基金产品；'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'2、33-46分，属于成长型的投资者。我们建议您考虑的投资产品应该可让资本金不被通货膨胀侵蚀，产品'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'预期收益率较高但价格波动性也高于保守型的投资者，您可以考虑部分介入风险程度较高的产品；'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'3、大于46分，属于进取型的投资者。我们建议您考虑的投资品的投资收益率远高于通货膨胀率，您可以'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'考虑持有风险程度较高的产品。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'五、风险程度确认'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'适合测试结果为“成长型”及“进取型”的投资者认购。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'如果您的测试结果属于上述类型，决定认购此基金产品，请签字确认：本人已经如实填写本《风险属性'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'评估问卷》，充分了解了自己的风险承受类型和适合购买的产品类型，并愿意承担相关风险。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*3
    text = u'投资者签名：______________________     日期：______________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*3
    text = u'本风险属性评估问卷结果是根据被调查人填写问卷时所提供的机构客户资料而推论得出，其结果将作为'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1
    text = u'被调查人，投资本机构基金产品的参考资料。此问卷内容及结果不构成与被调查人的要约，上海高毅资'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1
    text = u'产管理合伙企业（有限合伙）将不对此问卷的准确性及信息是否完整负责。上海高毅资产管理合伙企业'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1
    text = u'（有限合伙）明确规定所有获准使用此资料的员工均须遵守公司的保密责任。'
    c.drawString(inch,begy,text)

def DrawCanvasOrg1(c,clientID,date,qaArray):
    lineheight = 15
    client = Client.objects.get(client_id = clientID)
    c.setFont("jczt", 13)
    text = u'风险属性评估问卷(机构适用)'
    c.drawString(3*inch,11*inch,text)
    begy = 11*inch - lineheight*2
    c.setFont("msyh", 10)
    text = u'投资者姓名：    '+client.customer_name+'            填写日期：    '+date+'    '
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'风险提示：私募基金投资需承担各类风险，本金可能遭受损失。同时，私募基金投资还要考虑市场风险、'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'信用风险、流动性风险、操作风险等各类投资风险。您在基金认购过程中应当注意核对自己的风险识别和'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'风险承受能力，选择与自己风险识别能力和风险承受能力相匹配的私募基金。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'一、关于这份问卷：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       旨在协助贵公司了解自己对投资风险的承受度和投资目标，问卷信息将帮助我们提供适合贵公司的投'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'资产品供您参考。'
    c.drawString(inch,begy,text)


    begy = begy - lineheight
    text = u'       以下一系列问题可在您选择合适的私募基金前，协助评估您的风险承受能力、理财方式及投资目标：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       1、您是否为自己购买私募基金产品：  a.是；   b.不是'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       2、您是否符合以下合格投资者财务条件，即净资产不低于1000万元：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight
    text = u'       a.是；   b.不是'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'       投资人盖章确认：________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'二、投资人基本情况'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'       名称     ：'+client.customer_name+u'         法定代表人：________________________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1.5
    if client.id_no != '':
        if client.id_type == '0':
            text = u'       证件类型： 组织机构代码证       证件号码： '+client.id_no+''
        elif client.id_type == '1':
            text = u'       证件类型： 营业执照       证件号码： '+client.id_no+''
        elif client.id_type == '2':
            text = u'       证件类型： 行政机关       证件号码： '+client.id_no+''
        elif client.id_type == '3':
            text = u'       证件类型： 社会团体       证件号码： '+client.id_no+''
        elif client.id_type == '4':
            text = u'       证件类型： 军队       证件号码： '+client.id_no+''
        elif client.id_type == '5':
            text = u'       证件类型： 武警       证件号码： '+client.id_no+''
        elif client.id_type == '6':
            text = u'       证件类型： 下属机构（具有主管单位批文号）     证件号码： '+client.id_no+''
        elif client.id_type == '7':
            text = u'       证件类型： 基金会       证件号码： '+client.id_no+''
        elif client.id_type == '8':
            text = u'       证件类型： 其他       证件号码： '+client.id_no+''
    else:
        text = u'       证件类型：________________________________      证件号码：________________________________'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1.5
    text = u'       联系人   ：_____________________________        联系方式：________________________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'三、问卷题目'
    c.drawString(inch,begy,text)
    count = 0
    for line in qaArray:
        if count == 0 or count%6 == 0:
            begy = begy - lineheight*2
        else:
            begy = begy - lineheight*1
        c.drawString(inch,begy,line)
        count = count + 1

def DrawCanvasOrg2(c,qaArray):
    c.setFont("msyh", 10)
    lineheight = 15
    begy = 11.5*inch
    count = 0
    for line in qaArray:
        if len(line)>48:
            line1 = line[0:48]
            line2 = line[48:]
            begy = begy - lineheight*2
            c.drawString(inch,begy,line1)
            begy = begy - lineheight*1
            c.drawString(inch,begy,line2)
            count = count + 1
            continue
        if count == 0 or count%6 == 0:
            if count == 40:
                begy = begy - lineheight*1
            else:
                print count
                begy = begy - lineheight*2
        else:
            begy = begy - lineheight*1
        c.drawString(inch,begy,line)
        count = count + 1

def DrawCanvasOrg3(c,totalPoint):
    c.setFont("msyh", 10)
    lineheight = 15
    begy = 11.5*inch

    begy = begy - lineheight*2
    text = u'四、测试结果：'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = '得分：  ' + str(totalPoint)
    if totalPoint < 40:
        text = text + '        类型：保守型'
    elif totalPoint <= 60:
        text = text + '        类型：成长型'
    else:
        text = text + '        类型：进取型'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*2
    text = u'1、40分以下，属于保守型的投资者。可以考虑货币型等低风险产品，不适合风险程度较高的产品，考虑'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'到本基金产品“高风险、高收益”的特征，我们不建议贵公司考虑本基金产品；'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'2、40-60分，属于成长型的投资者。我们建议贵公司考虑的投资产品应该可让资本金不被通货膨胀侵蚀，'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'产品预期收益率较高但价格波动性也高于保守型的投资者，贵公司可考虑部分介入风险程度较高的产品；'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'3、大于60分，属于进取型的投资者。我们建议贵公司考虑的投资品的投资收益率远高于通货膨胀率，贵'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'公司可以考虑持有风险程度较高的产品。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'五、风险程度确认'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'适合测试结果为“成长型”及“进取型”的投资者认购。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*2
    text = u'如果贵公司的测试结果属于上述类型，决定认购此基金产品，请盖章确认：本公司已经如实填写本《风险'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*1
    text = u'属性评估问卷》，充分了解了自己的风险承受类型和适合购买的产品类型，并愿意承担相关风险。'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*3
    text = u'投资者盖章：______________________     日期：______________________'
    c.drawString(inch,begy,text)

    begy = begy - lineheight*3
    text = u'本风险属性评估问卷结果是根据被调查人填写问卷时所提供的机构客户资料而推论得出，其结果将作为'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1
    text = u'被调查人，投资本机构基金产品的参考资料。此问卷内容及结果不构成与被调查人的要约，上海高毅资'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1
    text = u'产管理合伙企业（有限合伙）将不对此问卷的准确性及信息是否完整负责。上海高毅资产管理合伙企业'
    c.drawString(inch,begy,text)
    begy = begy - lineheight*1
    text = u'（有限合伙）明确规定所有获准使用此资料的员工均须遵守公司的保密责任。'
    c.drawString(inch,begy,text)