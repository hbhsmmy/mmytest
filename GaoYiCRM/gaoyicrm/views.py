# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
import hashlib
import random
import requests
import operator
import tasvr_pb2 as tasver
import pbjson
import json
from models import UserInfo,Investor,Inquiry,Article,Message,Job,Customer,recommendedFund,UserRole
from django.core.paginator import Paginator

# url = 'http://115.159.154.36:10000'
url = 'http://127.0.0.1:10000'

#判断当前属于中文还是英文，并切换为相反语言
def changeVersions(request):
    if request.session['language'] == 'Chinese':
        request.session['language'] = 'English'
    elif request.session['language'] == 'English':
        request.session['language'] = 'Chinese'
    return JsonResponse({})

def changeToChinese(request):
    upDateRecommendedFund()
    request.session['language'] = 'Chinese'
    return JsonResponse({})

def changeToEnglish(request):
    request.session['language'] = 'English'
    return JsonResponse({})

#判断用户是否登陆
def loginOrNot(request):
    try:
        print request.session["user_id"]
        user = UserInfo.objects.get(user_id=request.session["user_id"])
        return JsonResponse({'loginOrNot':'1','username':user.user_name});
    except:
        return JsonResponse({'loginOrNot':'0','url':'../'})

#返回首页及新闻报道
def home(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        articles = Article.objects.filter(is_homepage = True)
        #choiceness对应精选，wealth对应财富观察
        choiceness = []
        wealth = []
        for item in articles.filter(type = 1):
            content = {'id':item.id,'title':item.title,'time':item.date_publish.strftime('%Y-%m-%d')}
            choiceness.append(content)
        for item in articles.filter(type = 2):
            content = {'id':item.id,'title':item.title,'time':item.date_publish.strftime('%Y-%m-%d')}
            wealth.append(content)
        # print choiceness,wealth
        content = {'choiceness':choiceness,"wealth":wealth}
        return render(request,'index.html',content)
    if request.session['language'] == 'English':
        return render(request,'index_en.html')

#返回公司介绍
def company(request):
    try:
        print request.session['language']
    except:
        request.session['language'] = 'Chinese'
    if request.session['language'] == 'Chinese':
        return render(request,"company.html")
    if request.session['language'] == 'English':
        return render(request,"company_en.html")


def versions(request):
    try:
        print request.session['language']
    except:
        request.session['language'] = 'Chinese'

#返回公司基金经理对应页面
def investTeam_qgl(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        return render(request,'investTeam_qgl.html')
    if request.session['language'] == 'English':
        return render(request,'investTeam_qgl_en.html')


def investTeam_dxf(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        return render(request,'investTeam_dxf.html')
    if request.session['language'] == 'English':
        return render(request,'investTeam_dxf_en.html')


def investTeam_sqr(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        return render(request,'investTeam_sqr.html')
    if request.session['language'] == 'English':
        return render(request,'investTeam_sqr_en.html')


def investTeam_zlw(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        return render(request,'investTeam_zlw.html')
    if request.session['language'] == 'English':
        return render(request,'investTeam_zlw_en.html')


def investTeam_fl(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        return render(request,'investTeam_fl.html')
    if request.session['language'] == 'English':
        return render(request,'investTeam_fl_en.html')


def investTeam_wsh(request):
    versions(request)
    if request.session['language'] == 'Chinese':
        return render(request,'investTeam_wsh.html')
    if request.session['language'] == 'English':
        return render(request,'investTeam_wsh_en.html')


def investTeam_news_qgl(request):
    return render(request,'investTeam_news_qgl.html')

def investTeam_news_qgl_info(request, articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'investTeam_news_qgl_info.html',{'info':info})

def investTeam_news_dxf(request):
    return render(request,'investTeam_news_dxf.html')

def investTeam_news_dxf_info(request, articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'investTeam_news_dxf_info.html',{'info':info})

def investTeam_news_sqr(request):
    return render(request,'investTeam_news_sqr.html')

def investTeam_news_sqr_info(request, articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'investTeam_news_sqr_info.html',{'info':info})

def investTeam_news_zlw(request):
    return render(request,'investTeam_news_zlw.html')

def investTeam_news_zlw_info(request, articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'investTeam_news_zlw_info.html',{'info':info})

def investTeam_news_fl(request):
    return render(request,'investTeam_news_fl.html')

def investTeam_news_fl_info(request, articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'investTeam_news_fl_info.html',{'info':info})

def investTeam_news_wsh(request):
    return render(request,'investTeam_news_wsh.html')

def investTeam_news_wsh_info(request, articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'investTeam_news_wsh_info.html',{'info':info})

#根据基金经理返回相关文章
def manageMedia(request):
    articles = Article.objects.filter(manager=request.GET['manager'])
    recommendArticles = []
    for item in articles:
        if item.is_recommend:
            details = {'id':item.id,'title':item.title,'brief_comment':item.brief_comment,'time':item.date_publish.strftime('%Y-%m-%d')}
            recommendArticles.append(details)
    articles = articles.filter(is_recommend=False)
    if request.GET['type'] == 'part':
        if len(articles) > 3:
            articles = articles[:3]
    if request.GET['type'] == 'all':
        articles_paginator = Paginator(articles,8)
        articles = articles_paginator.page(int(request.GET['page']))
    list = []
    for item in articles:
        details = {'id':item.id,'title':item.title,'time':item.date_publish.strftime('%Y-%m-%d')}
        list.append(details)
    if request.GET['type'] == 'part':
        content = {'articles':list,'recommendArticles':recommendArticles}
    if request.GET['type'] == 'all':
        content = {'articles':list,'totalcount':articles_paginator.num_pages,'recommendArticles':recommendArticles}
    return JsonResponse(content)

def trends_media(request):
    return render(request,'trends_media.html')

def trends_research(request):
    return render(request,'trends_research.html')

#根据类型返回相关文章，1：高毅精选，2：财富观察，以每页8条信息进行分页
def get_articles(request):
    articles = Article.objects.filter(type=int(request.GET['type']))
    articles_paginator = Paginator(articles,8)
    subArticlesPaginatorList = []
    for item in articles_paginator.page(int(request.GET['page'])):
        subArticlesPaginatorList.append(item)
    articlesTitle = []
    for item in subArticlesPaginatorList:
        content = {'id':item.id,'title':item.title,'time':item.date_publish.strftime('%Y-%m-%d')}
        articlesTitle.append(content)
    content = {'articlesTitle':articlesTitle,'totalcount':articles_paginator.num_pages,'len':len(articlesTitle)}
    return JsonResponse(content)

#根据文章编号返回具体文章内容
def trends_media_info(request,articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'trends_media_info.html',{'info':info})

def trends_research_info(request,articleID=1):
    info = Article.objects.get(id=articleID)
    return render(request,'trends_research_info.html',{'info':info})

def logout(request):
    try:
        del request.session['userID']
    except Exception:
        print Exception
    return JsonResponse({})

def account_details(request):
    return render(request,'account_details.html')

def account_home_info(request):
    return render(request,'account_home_info.html')

def account_editor(request):
    return render(request,'account_editor.html')

def account_org_editor(request):
    return render(request, 'account_org_editor.html')

def account_task(request):
    return render(request,'account_task.html')

def login(request):
    return render(request,"login.html")

def commitment(request):
    return render(request,"commitment.html")

def register(request):
    return render(request,"register.html")

def retrieve(request):
    return render(request,"retrieve.html")

def contact_information(request):
    try:
        print request.session['language']
    except:
        request.session['language'] = 'Chinese'
    if request.session['language'] == 'Chinese':
        return render(request,'contact_information.html')
    if request.session['language'] == 'English':
        return render(request,'contact_information_en.html')


def contact_recruitment(request):
    jobs = Job.objects.all()
    content = {'job':jobs}
    print content
    return render(request,'contact_recruitment.html',content)

def contact_recruitment_info(request, jobTitle="_"):
    job = Job.objects.get(id=jobTitle)
    return render(request,'contact_recruitment_info.html',{'job':job})

def account_home(request):
    return render(request, 'account_user_details.html')

def authentication(request, chooseType="_"):
    return render(request,"authentication.html")


#根据全部经理和默认排序获取公司产品
def account_product(request):
    try:
        print request.session["user_id"]
        return render(request,'account_product.html')
    except:
        return render(request,"login.html")

#进入预约列表，默认加载分页第一页内容
def accout_inquiry(request):
    try:
        print request.session["user_id"]
        return render(request,"account_inquiry.html")
    except:
        return render(request,"login.html")

#进入预约详情
def bespeak(request):
    return render(request,'account_bespeak.html')

#进入预约详情
def account_bespeak(request):
    return render(request,'account_bespeak2.html')

#进入客户列表，默认加载分页第一页内容
def account_records(request):
    try:
        print request.session["user_id"]
        return render(request,"account_records.html")
    except:
        return render(request,'login.html')

#获取选中基金名称
def get_ready_for_bespeak(request):
    request.session['choosedFund'] = request.GET['choosedFund']
    return JsonResponse({'url':'../account_bespeak'})

#问卷调查
def questionnaire(request):
    return render(request,"wenjuan.html")

def org_questionnaire(request):
    return render(request,"wenjuan_org.html")

#问卷调查
def riskEvaluation_result(request):
    return render(request,"riskEvaluation_result.html")

def org_riskEvaluation_result(request):
    return render(request,"riskEvaluation_result_org.html")

#储存预约信息
def store_inquery(request):

    investor = Investor.objects.get(id = request.session['userID'])
    new_userid = request.session['userID']
    new_realname = investor.realname
    new_email = investor.email
    new_mobile = request.GET['mobile']
    new_messgae = request.GET['message']
    new_inquirytype = request.GET['inquirytype']
    new_date = request.GET['date']
    new_time = request.GET['time']
    new_fundname = request.session['choosedFund']
    new_inquery = Inquiry(userid=new_userid, realname=new_realname, mobile=new_mobile,email=new_email, message = new_messgae, inquirytype=new_inquirytype, fundname=new_fundname, date=new_date, time=new_time, inquirystate=1)
    new_inquery.save()
    return JsonResponse({})

#删除预约信息
def delete_inquery(request):
    inquery = Inquiry.objects.filter(userid = request.session['userID']).filter(inquirystate = 1).filter(fundname = request.GET['fundName'].encode('utf-8'))
    inquery.delete()
    return JsonResponse({})

#判断是否可以查看基金净值和月报
def getAuthority(request):
    try:
        investor = Investor.objects.get(id = request.session['userID'])
        total = accountHomeRse(investor.taid)
        count = 0
        for item in total['fundlist']:
            if(item['fundid']==request.GET['fundid']):
                count = count+1
        if count!=0:
            content = {'authority':0}
        else:
            content = {'authority':1}
        return JsonResponse(content)
    except:
        return JsonResponse({})

def get_home(request):
    try:
        investor = Investor.objects.get(id = request.session['userID'])
        mobile = investor.mobile
        mobile = mobile.replace(mobile[3:7],"****")
        taid = investor.taid
        content = {'name':investor.username,"mobile":mobile}
        total = accountHomeRse(taid)
        content['assets'] = total['assets']
        content['totalreturn'] = total['totalreturn_money']
        content['lastweekreturn'] = total['totalreturn_rate']
        content['navday'] = total['navday']
        content['fundlist'] = total['fundlist']
        content['len'] = len(total['fundlist'])
        return JsonResponse(content)
    except:
        return render(request,"login.html")

#获取推荐基金的列表
def getRecommendedFunds(request):
    fund = recommendedFund.objects.all()
    recommendedFundsId = []
    recommendedFunds = []
    for item in fund:
        if item.isRecommended == True:
            recommendedFundsId.append(item.fundId)
    if len(recommendedFundsId) != 0:
        try:
            print request.session['allList']
        except:
            allList = get_all_product()
            request.session['allList'] = allList
        print recommendedFundsId
        for item1 in recommendedFundsId:
            for item2 in request.session['allList']:
                if item1 == item2['fundid']:
                    recommendedFunds.append(item2)
    content = {'recommendedFundsList':recommendedFunds,'len':len(recommendedFunds)}
    return JsonResponse(content)

import time
#根据基金经理和排列顺序分页获取公司产品
def get_product(request):
    manager = request.GET['manager']
    order = request.GET['order']
    px = True
    if request.GET['px'] == '1':
        px = False
    subproductlist = []
    allList = get_all_product()
    if manager.encode('utf-8') == '全部':
        for item in allList:
            subproductlist.append(item)
    else:
        for item in allList:
            if item['manager'].encode('utf-8') == manager.encode('utf-8'):
                subproductlist.append(item)
    if order.encode('utf-8') == '份额净值':
        subproductlist.sort(key = operator.itemgetter('nav'),reverse=px)
    elif order.encode('utf-8') == '周涨跌幅':
        subproductlist.sort(key = operator.itemgetter('weekreturn'),reverse=px)
    elif order.encode('utf-8') == '累计收益率':
        subproductlist.sort(key = operator.itemgetter('totalreturn'),reverse=px)
    elif order.encode('utf-8') == '成立时间':
        subproductlist.sort(key = operator.itemgetter('startday'),reverse=px)
    new_first_subproductlist = []
    try:
        search = request.GET['search']
        for item in subproductlist:
            if item['name'].encode('utf-8').find(search.encode('utf-8')) != -1:
                new_first_subproductlist.append(item)
    except:
        new_first_subproductlist = subproductlist
    new_second_subproductlist = []
    try:
        search = request.GET['type']
        for item in new_first_subproductlist:
            if search == '全部':
                new_second_subproductlist = new_first_subproductlist
            elif search == '母基金' and item['motherfund']:
                new_second_subproductlist.append(item)
            elif search == '子基金' and (not item['motherfund']):
                new_second_subproductlist.append(item)
    except:
        new_second_subproductlist = new_first_subproductlist
    productlist_paginator = Paginator(new_second_subproductlist,8)
    subproductPaginatorList = []
    for item in productlist_paginator.page(int(request.GET['page'])):
        subproductPaginatorList.append(item)
    content = {'productList':subproductPaginatorList,'pageCount':productlist_paginator.num_pages}
    return JsonResponse(content)

#4
def get_inquiry(request):
    try:
        inquiry = Inquiry.objects.filter(userid = request.session['userID'])
        # inquiry.sort(key = operator.itemgetter('inquirytime'),reverse=True)
        inquiry = sorted(inquiry, key=lambda Inquiry: Inquiry.inquirytime, reverse=True)
        inquiry_paginator = Paginator(inquiry,8)
        inquiryList = []
        for item in inquiry_paginator.page(request.GET['pagenum']):
            content_tem = {'type':item.inquirytype,'name':item.fundname,'time':item.inquirytime.strftime('%Y-%m-%d'),'state':item.inquirystate}
            inquiryList.append(content_tem)
        content = {'inquiryList':inquiryList,'len':len(inquiryList),'totalcount':inquiry_paginator.num_pages}
        # content = {'inquiryList':inquiryList,'len':0,'totalcount':inquiry_paginator.num_pages}
        return JsonResponse(content)
    except:
        return render(request,"login.html")

#5
def  account_personal(request):
    try:
        print "123000",request.session["user_id"]
        # investor = Investor.objects.get(id = request.session['userID'])
        # username = investor.username
        # realname = investor.realname
        # if realname == '_':
        #     content1 = {'identification_realname':False}
        #     realname = '未认证'
        #     idno = '未认证'
        # else:
        #     content1 = {'identification_realname':True}
        #     realname = realname.replace(realname[1:],"***")
        #     idno = investor.idno
        #     idno = idno.replace(idno[6:],"******")
        # email = investor.email
        # address = investor.address
        # education = investor.education
        # occupation = investor.occupation
        # if email == '_':
        #     a = {'identification_email':False}
        # else:
        #     a = {'identification_email':True}
        # if address == '_':
        #     b = {'identification_address':False}
        # else:
        #     b = {'identification_address':True}
        # if education == '_':
        #     c = {'identification_education':False}
        # else:
        #     c = {'identification_education':True}
        # content1.update(a)
        # content1.update(b)
        # content1.update(c)
        # email = email.replace(email[3:7],"****")
        # mobile = investor.mobile
        # mobile = mobile.replace(mobile[3:7],"****")
        #
        # totalPoint = 0
        # for point in (investor.point).split('.'):
        #     totalPoint += int(point)
        # if totalPoint <= 28:
        #     style = '保守型'
        # elif totalPoint >= 39:
        #     style = '积极型'
        # else:
        #     style = '稳健型'
        # content = {'username':username,"realname":realname,'idno':idno,'mobile':mobile,'email':email,'style':style,'education':education,'occupation':occupation,'address':address}
        # content.update(content1)
        # return render(request,"account_personal.html",content)
        return render(request,"account_personal.html")
    except:
        return render(request,"login.html")
    return render(request,"account_personal.html")


def fund_info(request):
    ta = tasver.WebFundDetailReq()
    ta.fundid = request.GET['fundid']
    print ta.fundid
    header = tasver.Header()
    header.cmd = 107
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)

    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        print headerRes.errCode
        oAccountRsp = tasver.WebFundDetailRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        content = {'fundinfo':json.loads(oAccountJon)}
        return JsonResponse(content)
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def fund_details(request):
    ta = tasver.WebFundAssetReq()
    ta.fundid = "S33180"
    ta.investorid = "DI1042"
    header = tasver.Header()
    header.cmd = 106
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)

    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        print headerRes.errCode
        oAccountRsp = tasver.WebFundAssetRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        print oAccountJon
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def fund_details_chart(request):
    page = request.GET['page']
    ta = tasver.WebFundDetailReq()
    ta.fundid = request.GET['fundid']
    header = tasver.Header()
    header.cmd = 107
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.WebFundDetailRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        detailInfo = json.loads(oAccountJon)

        nav_paginator = Paginator(detailInfo['fundNavlist'],10)
        # print detailInfo['fundNavlist']
        # totalnav_paginator = Paginator(detailInfo['totalnav'],10)
        # print totalnav_paginator
        sh300_paginator = Paginator(detailInfo['sh300'],10)
        gem_paginator = Paginator(detailInfo['gem'],10)
        subNavPaginatorList = []
        totalNavPaginatorList = []
        subsh300PaginatorList = []
        subgemPaginatorList = []
        for item in nav_paginator.page(int(page)):
            subNavPaginatorList.append(item)
        # for item in totalnav_paginator.page(int(page)):
        #     totalNavPaginatorList.append(item)
        for item in sh300_paginator.page(int(page)):
            subsh300PaginatorList.append(item)
        for item in gem_paginator.page(int(page)):
            subgemPaginatorList.append(item)
        paginatorlist = [subNavPaginatorList,subsh300PaginatorList,subgemPaginatorList]
        print paginatorlist
        content = {'detailInfo':detailInfo,'paginatorList':paginatorlist,'len':len(nav_paginator.page(int(page))),'pageCount':nav_paginator.num_pages}
        return JsonResponse(content)
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")


#检查用户名是否已经存在
def check_name(request):
    if Investor.objects.filter(username = request.GET['username']).exists():
        content = {'is_exist':1}
    else:
        content = {'is_exist':0}
    return JsonResponse(content)

#检查手机号码是否注册超过三次
def check_mobile(request):
    if Investor.objects.filter(mobile = request.GET['mobile']).count() >= 3:
        content = {'is_repeat':1}
    else:
        content = {'is_repeat':0}
    return JsonResponse(content)

#发送验证码到用户手机，标签1：注册，标签2：找回
def send_code(request):
    request.session['mobilecode'] = generate_verification_code()
    print request.session['mobilecode']
    url = 'http://211.147.244.114:9801/CASServer/SmsAPI/SendMessage.jsp'
    tag = request.GET['tag']
    if tag == '1':
        msg = "欢迎注册成为高毅资产会员，您的验证码为"+request.session['mobilecode']
    elif tag == '2':
        msg = "欢迎使用高毅资产找回服务，您的验证码为"+request.session['mobilecode']
    data = {"userid":64126,"password":"cellwcl","destnumbers":request.GET['mobile'],"msg":msg,"sendtime":""}
    result = requests.post(url,data=data)
    content = {'status_code':result.status_code}
    return JsonResponse(content)

#检查验证码是否正确
def check_code(request):
    a = request.GET['mobilecode']
    b = request.session['mobilecode']
    if a != b:
        content = {'is_coincident':1}
    else:
        content = {'is_coincident':0}
        del request.session['mobilecode']
    return JsonResponse(content)

#保存用户信息
def store_info(request):
    new_username = request.POST['uesrname']
    new_password = request.POST['password']
    new_mobile = request.POST['mobile']
    request.session['uesrname'] = new_username
    request.session['mobile'] = new_mobile
    try:
        new_user = Investor(username=new_username, password=hashed_password(new_password), mobile=new_mobile,realname='_', idtype = 0, idno='_', email='_', openid =request.session['openid'], taid='_',education='_',occupation='_',point='_',address='_',appendage='_')
    except:
        new_user = Investor(username=new_username, password=hashed_password(new_password), mobile=new_mobile,realname='_', idtype = 0, idno='_', email='_', openid ='_', taid='_',education='_',occupation='_',point='_',address='_',appendage='_')
    new_user.save()
    request.session['userID'] = new_user.id
    return JsonResponse({})

#检查身份证号是否已被注册
def check_identity_card(request):
    if Investor.objects.filter(idno = request.GET['idno']).exists():
        content = {'is_exist':1}
    else:
        content = {'is_exist':0}
    return JsonResponse(content)


#获取用户TA_ID并更新
def get_TAID(idtype, idno, name, moblie):
    ta = tasver.WebVerifyIdReq()
    ta.idtype = int(idtype)
    ta.idno = idno
    ta.name = unicode(name, "utf-8")
    ta.phone = moblie
    header = tasver.Header()
    header.cmd = 101
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)
    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)

    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.WebVerifyIdRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        return json.loads(oAccountJon)['id']
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")
        return "_"

#上传身份信息并获取TAID
def update_identity_card(request):
    name = request.GET['realname'].encode('utf-8')
    idtype = request.GET['idtype']
    idno = request.GET['idno'].encode('utf-8')
    moblie = '00000000000'
    taid = get_TAID(idtype=idtype,idno=idno,name=name,moblie=moblie)
    print taid
    print request.session['userID']
    investor = Investor.objects.get(id = request.session['userID'])
    investor.realname = name
    investor.idtype = idtype
    investor.idno = idno
    investor.taid = taid
    investor.save()
    if taid == "_":
        return JsonResponse({'result':"0"})
    else:
        return JsonResponse({'result':"1"})

#检查电话是否存在
def check_phone_exist(request):
    if Investor.objects.filter(mobile = request.GET['mobile']).exists():
        content = {'is_exist':1}
    else:
        content = {'is_exist':0}
    return JsonResponse(content)

#检查相关电话下是否已经录入身份信息
def check_identity_typed(request):
    request.session['mobile'] = request.GET['mobile']
    for object in Investor.objects.filter(mobile = request.session['mobile']):
        print object.idno
        username = object.username;
        if object.idno != "_":
            content = {'is_typed':0}
            return JsonResponse(content)

    content = {'is_typed':1,'username':username}
    return JsonResponse(content)

# 检查录入的身份信息是否匹配
def check_matched(request):
    realname = request.GET['realname']
    idno = request.GET['idno']
    for object in Investor.objects.filter(mobile = request.session['mobile']):
        if object.realname == realname and object.idno == idno :
            content = {'is_matched':1,'username':object.username}
            return JsonResponse(content)
    content = {'is_matched':0}
    return JsonResponse(content)

#修改密码
def update_password(request):
    username = request.POST['username']
    password = request.POST['password']
    user = UserInfo.objects.get(user_name = username)
    user.user_password = password
    user.save()
    return JsonResponse({'success':0})

#修改密码
def change_password(request):
    password = request.POST['password']
    investor = Investor.objects.get(id = request.session['userID'])
    investor.password = hashed_password(password)
    investor.save()
    return JsonResponse({'success':0})

#登陆网站
def user_login(request):
    nameOrMobile = request.POST['nameOrMobile']
    password = request.POST['password']
    login_state = authenticate(nameOrMobile = nameOrMobile, password = password)
    if login_state['success']:
        request.session['userID'] = login_state['content']
        user = UserInfo.objects.get(user_id = login_state['content'])
        userRoleList = UserRole.objects.filter(user_id = user.user_id)
        print userRoleList
        return JsonResponse({'success':0,'userRoleList':userRoleList})
    else:
        return JsonResponse({'success':1})

def loginPart(request):
    try:
        investor = Investor.objects.get(id = request.GET['id'])
        request.session['userID'] = investor.id
        return JsonResponse({'success':1})
    except:
        return JsonResponse({'success':0})

def chooseUser(request):
    investors = []
    for item in request.session['userIDs']:
        investor = Investor.objects.get(id = item)
        realname = investor.realname
        realname = realname.replace(realname[1:],"***")
        idno = investor.idno
        idno = idno.replace(idno[6:],"******")
        contact = {'id':item,'realname':realname,'idno':idno}
        investors.append(contact)
    print investors
    return JsonResponse({'investors':investors})

def bind_weixin(request):
    nameOrMobile = request.POST['nameOrMobile']
    password = request.POST['password']
    login_state = authenticate(nameOrMobile = nameOrMobile, password = password)
    if login_state['success']:
        request.session['userID'] = login_state['content']
        investor = Investor.objects.get(id=request.session["userID"])
        investor.openid =  request.session['openid']
        investor.save()
        return JsonResponse({'success':0})
    else:
        return JsonResponse({'success':1})

def user_logout(request):
    del request.session['user_id']
    return render(request,"login.html")

# 生成六位验证码
def generate_verification_code():
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    myslice = random.sample(code_list, 6)
    verification_code = ''.join(myslice)
    return verification_code

#利用MD5加密
def hashed_password(password=None):
    return hashlib.md5(password).hexdigest()

#验证信息
def authenticate(nameOrMobile = None, password = None):
    # user = True
    if Investor.objects.filter(username = nameOrMobile).exists():
        investor = Investor.objects.get(username = nameOrMobile)
        if investor.password == password:
            return {'success':True,'content':investor.id}
        else:
            return {'success':False}
    else:
        return {'success':False}
        # elif Investor.objects.filter(idno = nameOrMobile).exists():
        #     investor = Investor.objects.get(idno = nameOrMobile)
        # elif Investor.objects.filter(mobile = nameOrMobile).exists():
        #     if len(Investor.objects.filter(mobile = nameOrMobile)) == 1:
        #         investor = Investor.objects.get(mobile = nameOrMobile)
        #     else:
        #         investor = Investor.objects.filter(mobile = nameOrMobile)
        #         user = False

        # to_hashed_password = hashed_password(password)
        # if user:
        #     if investor.password == to_hashed_password:
        #         return {'success':True,'content':investor.id,'special':False}
        # else:
        #     investors = []
        #     for item in investor:
        #         if item.password == to_hashed_password:
        #             investors.append(item.id)
        #     print len(investors)
        #     if len(investors) == 1:
        #         return {'success':True,'content':investors[0],'special':False}
        #     elif len(investors) == 2 | len(investors) == 3:
        #         return {'success':True,'content':investors,'special':True}
        # return {'success':False}

#留言
def leave_message(request):
    new_username = request.GET['username']
    new_mobile = request.GET['mobile']
    new_email = request.GET['email']
    new_message = request.GET['message']
    new_date = request.GET['date']
    new_time = request.GET['time']
    message = Message(username=new_username,mobile=new_mobile,email=new_email,message=new_message,date=new_date,time=new_time)
    message.save()
    customers = Customer.objects.filter(status=0)
    if len(customers)>0:
        sendCustomerMessage(customers,message)
    else:
        customers = Customer.objects.all()
        for item in Customer.objects.all():
            item.status = 0
            item.save()
        sendCustomerMessage(customers,message)
    return JsonResponse({})

def sendCustomerMessage(customers,message):
    for item in customers:
        url = 'http://211.147.244.114:9801/CASServer/SmsAPI/SendMessage.jsp'
        msg = '姓名为'+message.username.encode("utf-8")+'，电话为'+message.mobile.encode("utf-8")+'的客户留言，内容：'+message.message.encode("utf-8") +'。预约'+message.date.encode("utf-8")+'的'+message.time.encode("utf-8")+'。'
        data = {"userid":64126,"password":"cellwcl","destnumbers":item.mobile,"msg":msg,"sendtime":""}
        requests.post(url,data=data)
        item.status = 1
        item.save()
        break


def check_status(request):
    if request.session["user_id"] == None:
        return render(request,"login.html");
    else:
        return render(request, "account_user_details.html",{'name':"tanmoumou"});

def accountHomeRse(taid,time):
    ta = tasver.AccountHomeReq()
    ta.investorid = taid
    ta.reqday = time
    header = tasver.Header()
    header.cmd = 104
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)

    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.AccountHomeRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        print json.loads(oAccountJon)
        return json.loads(oAccountJon)

    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def webFundAssetReq(taid):
    ta = tasver.WebFundAssetReq()
    ta.fundid = "S33180"
    ta.investorid = "DI1042"
    header = tasver.Header()
    header.cmd = 106
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.WebFundAssetRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        return json.loads(oAccountJon)
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def get_all_product():
    ta = tasver.ProductListReq()
    header = tasver.Header()
    header.cmd = 102
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)
    headers = {'content-type': 'application/json'}
    print '!!!!!!!begin',time.time()
    r = requests.post(url,headdata,headers=headers)
    print '!!!!!!!end',time.time()
    headerRes = tasver.WebRspHeader()
    print '____________step1',time.time()
    headerRes.ParseFromString(r.content)
    print '____________step2',time.time()
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.ProductListRsp()
        print '____________step3',time.time()
        oAccountRsp.ParseFromString(headerRes.content)
        print '____________step4',time.time()
        oAccountJon = pbjson.pb2json(oAccountRsp)
        print '____________step5',time.time()
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")
    print '____________step6',time.time()
    alllist = json.loads(oAccountJon)['productlist']
    print alllist
    print '____________step7',time.time()
    return alllist

# def get_records(request):
#     investor = Investor.objects.get(id = request.session['userID'])
#     ta = tasver.WebOpRecordReq()
#     ta.investorid = investor.taid
#     header = tasver.Header()
#     header.cmd = 103
#     header.ver = 0
#     header.platform = 3
#     header.content = pbjson.pb2json(ta)
#     headdata = pbjson.pb2json(header)
#
#     headers = {'content-type': 'application/json'}
#     r = requests.post(url,headdata,headers=headers)
#     headerRes = tasver.WebRspHeader()
#     headerRes.ParseFromString(r.content)
#     if headerRes.errCode == 0 :
#         oAccountRsp = tasver.WebOpRecordRsp()
#         oAccountRsp.ParseFromString(headerRes.content)
#         oAccountJon = pbjson.pb2json(oAccountRsp)
#     else :
#         print "ErrCode:"
#         print headerRes.errCode
#         print "ErrMsg:"
#         print headerRes.errMsg.encode("utf-8")
#     records =  json.loads(oAccountJon)
#     funds = []
#     for item in records['op']:
#         if {'fundname':item['fundname'],'fundid':item['fundid']} not in funds:
#             fund = {'fundname':item['fundname'],'fundid':item['fundid']}
#             funds.append(fund)
#     content = {'funds':funds,'fundsCount':len(funds),'recordsList':records['op'],'len':len(records['op'])}
#     return JsonResponse(content)

def get_records(ta_id):
    ta = tasver.WebOpRecordReq()
    ta.investorid = ta_id
    header = tasver.Header()
    header.cmd = 103
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.WebOpRecordRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")
    records =  json.loads(oAccountJon)
    funds = []
    for item in records['op']:
        if {'fundname':item['fundname'],'fundid':item['fundid']} not in funds:
            fund = {'fundname':item['fundname'],'fundid':item['fundid']}
            funds.append(fund)
    content = {'funds':funds,'fundsCount':len(funds),'recordsList':records['op'],'len':len(records['op'])}
    return content

def upDateRecommendedFund():
    fund = recommendedFund.objects.all()
    allList = get_all_product()
    if len(fund) < len(allList):
        for item in allList:
            if item not in fund:
                new_fund = recommendedFund(fundId=item['fundid'], fundName=item['name'].encode('utf-8'), isRecommended=False)
                new_fund.save()
