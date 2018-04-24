# -*- coding: utf-8 -*-
__author__ = 'zhangchengyiming'
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from views import accountHomeRse,get_records,get_all_product
from utils import get_time,get_time_details,creatNewPDF,createOrgPDF
from models import UserInfo,Client,InterestManager,Dictionary,Contact,ContactClient,Message,Apply,Accredited,AccreditedDoc,Document,ClientAccount,Capital,ApplyCapital,ApplyContact
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from suds.client import Client as TAClient
import tasvr_pb2 as tasver
import json
import pbjson
import requests
import sys
import xlwt
import datetime as DTtime
import os
import calendar
from datetime import datetime

import threading
import numpy
import time
import base64
import operator

reload(sys)
sys.setdefaultencoding( "utf-8" )

url = 'http://127.0.0.1:10000'
# url = 'http://115.159.154.36:10000'

def task_detail(request):
    return render(request,'account_task_detail.html')

def message_detail(request):
    return render(request,'account_message_detail.html')

def account_function(request):
    return render(request,'account_function.html')

def account_upload(request):
    return render(request,'account_upload.html')

def get_task_detail(request):
    contactClient = ContactClient.objects.get(contact_id = request.GET['contact_id'])
    contact = Contact.objects.get(contact_id = request.GET['contact_id'])
    client = Client.objects.get(client_id =contactClient.client_id)
    content = {'contact_id':contact.contact_id,'client_id':client.client_id,'contact_type':contact.contact_type,'contact_date':contact.contact_date,'contact_detail':contact.contact_detail,'contact_type':contact.contact_type,'customer_name':client.customer_name,'customer_mobile':client.mobile,'customer_email':client.customer_email,'status':contact.task_status,'contact_record':contact.contact_record,'record_date':contact.record_date,'updated_by':contact.updated_by}
    return JsonResponse(content)

def get_detail_message(request):
    message = Message.objects.get(message_id = request.GET['message_id'])
    content = {'message_id':message.message_id,'message_time':message.message_time,'message_username':message.username,'message_mobile':message.mobile,'message_email':message.email,'contact_date':message.contact_date,'contact_time':message.contact_time,'message':message.message}
    return JsonResponse(content)

#进入客户列表，默认加载分页第一页内容
def account_records(request):
    try:
        print request.session["user_id"]
        return render(request,"account_records.html")
    except:
        return render(request,'login.html')

def get_user_count(request):
    return JsonResponse({'len':Client.objects.count()})

def get_client_list(request):
    clientsList = Client.objects.all().order_by('-client_id')
    content = client_list(clientsList,int(request.GET['page']))
    return JsonResponse(content)

def search_classify_user(request):
    search = request.GET['content']
    Khlx = request.GET['Khlx']
    Khqd = request.GET['Khqd']
    Khzt = request.GET['Khzt']
    Jjjl = request.GET['Jjjl']
    if Jjjl != '0':
        clients = Client.objects.filter(interestmanager__manager_id__contains= int(Jjjl))
    else:
        clients = Client.objects.all()
    if Khlx != '9' and Khqd == '0' and Khzt == '0':
        clients = clients.filter(customer_type = Khlx)
    if Khlx == '9' and Khqd != '0' and Khzt == '0':
        clients = clients.filter(source_type = Khqd)
    if Khlx == '9' and Khqd == '0' and Khzt != '0':
        clients = clients.filter(mark = Khzt)
    if Khlx != '9' and Khqd != '0' and Khzt == '0':
        clients = clients.filter(customer_type = Khlx, source_type = Khqd)
    if Khlx != '9' and Khqd == '0' and Khzt != '0':
        clients = clients.filter(customer_type = Khlx, mark = Khzt)
    if Khlx == '9' and Khqd != '0' and Khzt != '0':
        clients = clients.filter(source_type = Khqd, mark = Khzt)
    if Khlx != '9' and Khqd != '0' and Khzt != '0':
        clients = clients.filter(customer_type = Khlx, source_type = Khqd, mark = Khzt)
    if search != "":
        clients_search = clients.filter(Q(customer_name__contains = search)|Q(id_no__contains = search)|Q(mobile__contains = search)|Q(contact_name__contains = search)|Q(contact_mobile__contains = search))
        content = client_list(clients_search.order_by('-client_id'),int(request.GET['page']))
    else:
        content = client_list(clients.order_by('-client_id'),int(request.GET['page']))
    print content
    return JsonResponse(content)

def search_user(request):
    search = request.GET['content']
    clients_search = Client.objects.filter(Q(customer_name__contains = search)|Q(id_no__contains = search)|Q(mobile__contains = search)|Q(contact_name__contains = search)|Q(contact_mobile__contains = search))
    content = client_list(clients_search.order_by('-client_id'),int(request.GET['page']))
    return JsonResponse(content)

def get_client_classify(request):
    Khlx = request.GET['Khlx']
    Khqd = request.GET['Khqd']
    Khzt = request.GET['Khzt']
    Jjjl = request.GET['Jjjl']
    if Jjjl != '0':
        clients = Client.objects.filter(interestmanager__manager_id__contains= int(Jjjl))
    else:
        clients = Client.objects.all()
    if Khlx != '9' and Khqd == '0' and Khzt == '0':
        clients = clients.filter(customer_type = Khlx)
    if Khlx == '9' and Khqd != '0' and Khzt == '0':
        clients = clients.filter(source_type = Khqd)
    if Khlx == '9' and Khqd == '0' and Khzt != '0':
        clients = clients.filter(mark = Khzt)
    if Khlx != '9' and Khqd != '0' and Khzt == '0':
        clients = clients.filter(customer_type = Khlx, source_type = Khqd)
    if Khlx != '9' and Khqd == '0' and Khzt != '0':
        clients = clients.filter(customer_type = Khlx, mark = Khzt)
    if Khlx == '9' and Khqd != '0' and Khzt != '0':
        clients = clients.filter(source_type = Khqd, mark = Khzt)
    if Khlx != '9' and Khqd != '0' and Khzt != '0':
        clients = clients.filter(customer_type = Khlx, source_type = Khqd, mark = Khzt)
    content = client_list(clients.order_by('-client_id'),int(request.GET['page']))
    return JsonResponse(content)

def client_list(clients,page):
    clients_len = clients.count()
    clients_paginator = Paginator(clients,8)
    clients = clients_paginator.page(int(page))

    contacts = ContactClient.objects.filter(contact__task_status__contains='2')
    channelList = get_user_channel(clients)['usrchannels']
    clientsPaginatorList = []
    for item in clients:
        count = 0
        for contact in contacts:
            if item.client_id == contact.client_id:
                count = count + 1
        content = {'id':item.client_id,'name':item.customer_name,'sex':item.sex,'type':item.customer_type,'id_no':item.id_no,'contact_count':count,
                   'customer_mobile':item.mobile,'customer_channels':'','contact_name':item.contact_name,'contact_mobile':item.contact_mobile}
        for channel in channelList:
            if item.ta_id == channel['investorid']:
                content['customer_channels'] = channel['channels']
        clientsPaginatorList.append(content)
    return {'clientsList':clientsPaginatorList,'pageCount':clients_paginator.num_pages,'len':clients_len}

def get_user_details(request):
    client = Client.objects.get(client_id = request.GET['clientID'])
    try:
        client_channel = get_user_channel([client])['usrchannels'][0]['channels']
        client_channels = ' '.join(client_channel)
    except:
        client_channels = ''
    try:
        total = accountHomeRse(client.ta_id,get_time())
    except:
        total = ""
    try:
        trade = get_records(client.ta_id)
    except:
        trade = ""
    contactClientList = ContactClient.objects.filter(client_id = request.GET['clientID'])
    managerList = InterestManager.objects.filter(client_id = request.GET['clientID'])
    contactList = []
    for item in contactClientList:
        contact = Contact.objects.get(contact_id=item.contact_id)
        user = UserInfo.objects.get(user_id = contact.contact_user_id)
        content = {'contact_id':contact.contact_id,'task_date':contact.contact_date,'contact_user':user.user_name,'contact_detail':contact.contact_detail,'contact_record':contact.contact_record,'note':contact.note,'task_status':contact.task_status,'contact_type':contact.contact_type}
        if contact.task_status == '1':
            content['task_date'] = contact.record_date
        contactList.insert(0,content)
    client_managers = ''
    for item in managerList:
        result = Dictionary.objects.get(type = '基金经理',value = item.manager_id)
        client_managers = client_managers + result.name + '  '
    page1 = {'customer_name':client.customer_name,'mark':client.mark,'customer_manager':client.customer_manager,'customer_src':client.client_source_desc,
             'created_by':client.created_by,'created_date':str(client.created_date)[0:10],
             'updated_by':client.updated_by,'updated_date':str(client.updated_date)[0:10],
             'customer_mobile':client.mobile,'customer_email':client.customer_email,
             'education':client.education,'occupation':client.occupation,'employer':client.employer,'businessscope':client.businessscope,
             'represent1':client.represent1,'represent_idtype':client.represent_idtype,'represent_idno':client.represent_idno,'controller':client.controller,
             'province':client.province,'city':client.city,'address':client.address,'investor_name':client.username,'customer_wx':client.customer_wx,
             'contact_name':client.contact_name,'contact_mobile':client.contact_mobile,
             'customer_managers':client_managers,'customer_interest':client.interest,'client_type':client.customer_type,
             'card_type':client.id_type,'card_no':client.id_no,'customer_channel':client_channels,'ta_id':client.ta_id,}
    if total == "" or total == None:
        page2 = ""
    else:
        page2 = {'assets':total['assets'],'totalreturn_money':total['totalreturn_money'],'totalreturn_rate':total['totalreturn_rate'],
                 'fundlist':total['fundlist']}
    page4 = {'contactList':contactList,'contactList_len':len(contactList)}
    content = {'page1':page1,'page2':page2,'page3':trade,'page4':page4}
    return JsonResponse(content)

def get_user_channel(clients):
    ta = tasver.ChannelReq()
    for item in clients:
        try:
            ta.investorid.append(item.ta_id);
        except:
            print 'sorry,there is no taID'
    header = tasver.Header()
    header.cmd = 111
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)

    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    print '------',time.time()
    r = requests.post(url,headdata,headers=headers)
    print '------',time.time()
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.ChannelRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        print '-------------',json.loads(oAccountJon)
        return json.loads(oAccountJon)
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def edit_email_client(request):
    print '--------------------'
    print request.GET['id_no']
    print request.GET['email']
    client = Client.objects.get(id_no = request.GET['id_no'])
    client.customer_email = request.GET['email']
    client.save()
    return JsonResponse({'success':200})

def edit_crm_client(request):
    try:
        userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    except:
        try:
            if request.GET['channel'] == 'gaoyiweb':
                userinfo = UserInfo.objects.get(user_id = 1003)
        except:
            return JsonResponse({'success':402,'message':{}})
    client_org_holder = request.GET['client_org_holder']
    client_org_range = request.GET['client_org_range']
    client_legal_name = request.GET['client_legal_name']
    client_legal_type = request.GET['client_legal_type']
    client_legal_no = request.GET['client_legal_no']
    client_name = request.GET['client_name']
    client_phone = request.GET['client_phone']
    client_brithday = request.GET['client_brithday']
    client_nationality = request.GET['client_nationality']
    client_education  = request.GET['client_education']
    client_zipcode = request.GET['client_zipcode']
    client_occupation = request.GET['client_occupation']
    client_position = request.GET['client_position']
    client_employer   = request.GET['client_employer']
    contact_name = request.GET['contact_name']
    contact_phone = request.GET['contact_phone']
    client_email = request.GET['client_email']
    client_other = request.GET['client_other']
    client_validbegin = request.GET['client_validbegin']
    client_validend = request.GET['client_validend']
    province = request.GET['province']
    city = request.GET['city']
    address = request.GET['address']
    card_type = request.GET['card_type']
    sex = request.GET['sex']
    card_no = request.GET['card_no']
    client_type = request.GET['client_type']
    focuse_message = request.GET['focuse_message']
    managers= request.GET['manager_value']
    manager_list = managers.split(".")
    new_built = request.GET['build']
    if Client.objects.filter(id_no = card_no).exists():
        new_built = 'old'
    if new_built == "new":
        client = Client(mark='2',controller=client_org_holder,businessscope=client_org_range,customer_name=client_name,customer_type=client_type,id_type=card_type,id_no=card_no,sex=sex,
                        mobile=client_phone,customer_email=client_email,customer_wx=client_other,birthday=client_brithday,
                        nationality=client_nationality, education=client_education,zipcode=client_zipcode,occupation=client_occupation,position= client_position,employer=client_employer,
                        contact_name=contact_name,contact_mobile=contact_phone,
                        valid_begin=client_validbegin,valid_end=client_validend,
                        represent1=client_legal_name,represent_idtype=client_legal_type,represent_idno=client_legal_no,interest=focuse_message,
                        province=province,city=city,address=address,source_type=3,
                        created_by = userinfo.user_name, updated_by = userinfo.user_name)
        client.save()
        if manager_list != ['']:
            for item in manager_list:
                interestManager = InterestManager(client_id = client.client_id,manager_id = item, created_by = userinfo.user_name, updated_by = userinfo.user_name)
                interestManager.save()
        createAccredited(request,'',True,client)
        return JsonResponse({'success':200,'message':{'client_id':client.client_id,'client_name':client.customer_name,'url':'0'}})
    else:
        client = Client.objects.get(id_no = card_no)
        managerList = InterestManager.objects.filter(client_id = client.client_id)
        if client.mark != '1':
            client.customer_name = client_name
            client.customer_type = client_type
            client.id_type = card_type
            client.id_no = card_no
            client.sex = sex
        client.birthday = client_brithday
        client.nationality = client_nationality
        client.education = client_education
        client.zipcode = client_zipcode
        client.position = client_position
        client.occupation = client_occupation
        client.employer = client_employer
        client.controller = client_org_holder
        client.businessscope = client_org_range
        client.valid_begin = client_validbegin
        client.valid_end = client_validend
        client.represent1 = client_legal_name
        client.represent_idtype = client_legal_type
        client.represent_idno = client_legal_no
        client.mobile = client_phone
        client.customer_email = client_email
        client.customer_wx = client_other
        client.contact_name = contact_name
        client.contact_mobile = contact_phone
        client.interest = focuse_message
        client.province = province
        client.city = city
        client.address = address
        try:
            client.save()
        except:
            print 'No Change'
        address = unicode(str(client.province+client.city+client.address),'utf-8')
        SoapMessage ={"customer":{"customerName":unicode(str(client.customer_name),'utf-8'),
                                  "customerCode":client.id_no,
                                  "customerMobile":client.mobile,
                                  "customerEmail":client.customer_email,
                                  "customerAddress":address,
                                  "contactName":unicode(str(client.contact_name),'utf-8'),
                                  "contactMobile":client.contact_mobile,
                                  "modifiedUserName":unicode(str(userinfo.user_name),'utf-8')}}
        try:
            pass
        except:
            print 'send error'
        InterestManager.objects.filter(client_id = client.client_id).delete()
        if manager_list != ['']:
            for item in manager_list:
                interestManager = InterestManager(client_id = client.client_id,manager_id = item, created_by = userinfo.user_name, updated_by = userinfo.user_name)
                interestManager.save()
        try:
            accreditedList = Accredited.objects.filter(client_id = client.client_id,status =1)
            for item in accreditedList:
                if item.failed_type.find('0') < 0 :
                    if client.id_no == '':
                        faildType = '0|'+item.failed_type
                        print faildType
                elif item.failed_type.find('0') >= 0 and client.id_no != '' and client.id_no != None:
                    faildType = item.failed_type[2:]
                    print faildType
                item.failed_type = faildType
                item.save()
        except:
            pass
        return JsonResponse({'success':200,'message':{'client_id':client.client_id,'client_name':client.customer_name,'url':'1'}})

def edit_client(request):
    try:
        userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    except:
        try:
            if request.GET['channel'] == 'gaoyiweb':
                userinfo = UserInfo.objects.get(user_id = 1003)
        except:
            return JsonResponse({'success':402,'message':{}})
    print("aaaa")
    client_org_holder = request.GET['client_org_holder']
    client_org_range = request.GET['client_org_range']
    client_legal_name = request.GET['client_legal_name']
    client_legal_type = request.GET['client_legal_type']
    client_legal_no = request.GET['client_legal_no']
    client_name = request.GET['client_name']
    client_phone = request.GET['client_phone']
    client_brithday = request.GET['client_brithday']
    client_nationality = request.GET['client_nationality']
    client_education  = request.GET['client_education']
    client_zipcode = request.GET['client_zipcode']
    client_occupation = request.GET['client_occupation']
    client_position = request.GET['client_position']
    client_employer   = request.GET['client_employer']
    contact_name = request.GET['contact_name']
    contact_phone = request.GET['contact_phone']
    client_email = request.GET['client_email']
    client_other = request.GET['client_other']
    client_validbegin = request.GET['client_validbegin']
    client_validend = request.GET['client_validend']
    province = request.GET['province']
    city = request.GET['city']
    address = request.GET['address']
    card_type = request.GET['card_type']
    sex = request.GET['sex']
    card_no = request.GET['card_no']
    client_type = request.GET['client_type']
    focuse_message = request.GET['focuse_message']
    managers= request.GET['manager_value']
    manager_list = managers.split(".")
    print("bbbbb")
    try:
        username = request.GET['username']
    except:
        username = client_phone

    try:
        password = request.GET['password']
    except:
        password = hashed_password(str(client_phone)[-8:])

    try:
        openid = request.GET['openid']
    except:
        openid = ''

    try:
        taid = request.GET['taid']
    except:
        taid = ''
    print("ccccc")
    if not Client.objects.filter(id_no = card_no).exists():
        client = Client(mark='2',controller=client_org_holder,businessscope=client_org_range,customer_name=client_name,customer_type=client_type,id_type=card_type,id_no=card_no,sex=sex,
                        mobile=client_phone,customer_email=client_email,customer_wx=client_other,birthday=client_brithday,
                        nationality=client_nationality, education=client_education,zipcode=client_zipcode,occupation=client_occupation,position= client_position,employer=client_employer,
                        contact_name=contact_name,contact_mobile=contact_phone,
                        username = username,password = password,open_id = openid, ta_id = taid,
                        valid_begin=client_validbegin,valid_end=client_validend,
                        represent1=client_legal_name,represent_idtype=client_legal_type,represent_idno=client_legal_no,interest=focuse_message,
                        province=province,city=city,address=address,source_type=3,
                        created_by = userinfo.user_name, updated_by = userinfo.user_name)
        print("ddddddd")
        client.save()
        if manager_list != ['']:
            for item in manager_list:
                interestManager = InterestManager(client_id = client.client_id,manager_id = item, created_by = userinfo.user_name, updated_by = userinfo.user_name)
                interestManager.save()
        createAccredited(request,'',True,client)
        return JsonResponse({'success':200,'message':{'client_id':client.client_id,'client_name':client.customer_name,'url':'0'}})
    else:
        client = Client.objects.get(id_no = card_no)
        managerList = InterestManager.objects.filter(client_id = client.client_id)
        if client.mark != '1':
            client.customer_name = client_name
            client.customer_type = client_type
            client.id_type = card_type
            client.id_no = card_no
            client.sex = sex
        client.username = username
        client.password = password
        client.open_id = openid
        client.ta_id = taid
        client.birthday = client_brithday
        client.nationality = client_nationality
        client.education = client_education
        client.zipcode = client_zipcode
        client.position = client_position
        client.occupation = client_occupation
        client.employer = client_employer
        client.controller = client_org_holder
        client.businessscope = client_org_range
        client.valid_begin = client_validbegin
        client.valid_end = client_validend
        client.represent1 = client_legal_name
        client.represent_idtype = client_legal_type
        client.represent_idno = client_legal_no
        client.mobile = client_phone
        client.customer_email = client_email
        client.customer_wx = client_other
        client.contact_name = contact_name
        client.contact_mobile = contact_phone
        client.interest = focuse_message
        client.province = province
        client.city = city
        client.address = address
        try:
            client.save()
        except:
            print 'No Change'
        address = unicode(str(client.province+client.city+client.address),'utf-8')
        SoapMessage ={"customer":{"customerName":unicode(str(client.customer_name),'utf-8'),
                                  "customerCode":client.id_no,
                                  "customerMobile":client.mobile,
                                  "customerEmail":client.customer_email,
                                  "customerAddress":address,
                                  "contactName":unicode(str(client.contact_name),'utf-8'),
                                  "contactMobile":client.contact_mobile,
                                  "modifiedUserName":unicode(str(userinfo.user_name),'utf-8')}}
        try:
            pass
        except:
            print 'send error'
        InterestManager.objects.filter(client_id = client.client_id).delete()
        if manager_list != ['']:
            for item in manager_list:
                interestManager = InterestManager(client_id = client.client_id,manager_id = item, created_by = userinfo.user_name, updated_by = userinfo.user_name)
                interestManager.save()
        logcat = open("logcat.txt", 'a')
        #logcat.write('DetailsAfter:customer_name:'+str(client.customer_name)+' customer_type:'+str(client.customer_type)+' id_type:'+str(client.id_type)+' id_no:'+str(client.id_no)+' sex:'+str(client.sex)+' customer_mobile:'+str(client.mobile)+' customer_email:'+str(client.customer_email)+' customer_wx:'+str(client.customer_wx)+' contact_name:'+str(client.contact_name)+' contact_mobile:'+str(client.contact_mobile)+' province:'+str(client.province)+' city:'+str(client.city)+' address:'+str(client.address)+' source_type:'+str(client.source_type)+' interest:'+str(client.interest)+' created_by:'+str(client.created_by)+' updated_by:'+str(client.updated_by)+' managers:')
        if manager_list != ['']:
            for item in manager_list:
                logcat.write(str(item)+' ')
        logcat.write('\n')
        logcat.write('-------------------')
        logcat.write('\n')
        logcat.close()
        try:
            accreditedList = Accredited.objects.filter(client_id = client.client_id,status =1)
            for item in accreditedList:
                print '_________________',item.failed_type.find('0')
                if item.failed_type.find('0') < 0 :
                    if client.id_no == '':
                        faildType = '0|'+item.failed_type
                        print faildType
                elif item.failed_type.find('0') >= 0 and client.id_no != '' and client.id_no != None:
                    faildType = item.failed_type[2:]
                    print faildType
                item.failed_type = faildType
                item.save()
        except:
            pass
        return JsonResponse({'success':200,'message':{'client_id':client.client_id,'client_name':client.customer_name,'url':'1'}})

import hashlib
# 利用MD5加密
def hashed_password(password=None):
    return hashlib.md5(password).hexdigest()

#获取客户资料
def get_user_edit(request):
    client = Client.objects.get(client_id=request.GET['client_id'])
    managerList = InterestManager.objects.filter(client_id = request.GET['client_id'])
    documentList = check_info(request.GET['client_id'])
    client_managers = ''
    if managerList.exists():
        for item in managerList:
            client_managers = client_managers + item.manager_id + '.'
    content = {'client_org_holder':client.controller,'client_org_range':client.businessscope, 'client_legal_name':client.represent1,'client_legal_type':client.represent_idtype,'represent_idno':client.represent_idno,
               'mark':client.mark,'client_name':client.customer_name,'sex':client.sex,'client_type':client.customer_type,'card_type':client.id_type,'card_no':client.id_no,'client_brithday':client.birthday,
               "client_nationality":client.nationality,'client_education':client.education,'client_zipcode':client.zipcode,
               'client_occupation':client.occupation,'client_position':client.position,'client_employer':client.employer,
               'client_phone':client.mobile,'client_email':client.customer_email,'client_other':client.customer_wx,'client_validbegin':client.valid_begin,'client_validend':client.valid_end,
               'contact_name':client.contact_name,'contact_phone':client.contact_mobile,'province':client.province,'city':client.city,'address':client.address,
               'focuse_message':client.interest,'manager_value':client_managers,'client_risk_type':client.risk_type,'documentList':documentList}
    return JsonResponse(content)

def delet_client(request):
    try:
        userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    except:
        return JsonResponse({'success':402,'message':{}})
    client = Client.objects.get(client_id=request.GET['client_id'])
    managerList = InterestManager.objects.filter(client_id = request.GET['client_id'])
    logcat = open("logcat.txt", 'a')
    #logcat.write('Time:'+str(get_time_details())+'  '+'User:'+str(userinfo.user_name)+'\n')
    #logcat.write('Action:Remove the client with ID '+str(client.client_id)+'\n')
    #logcat.write('DetailsBefore:customer_name:'+str(client.customer_name)+' customer_type:'+str(client.customer_type)+' id_type:'+str(client.id_type)+' id_no:'+str(client.id_no)+' sex:'+str(client.sex)+' customer_mobile:'+str(client.mobile)+' customer_email:'+str(client.customer_email)+' customer_wx:'+str(client.customer_wx)+' contact_name:'+str(client.contact_name)+' contact_mobile:'+str(client.contact_mobile)+' province:'+str(client.province)+' city:'+str(client.city)+' address:'+str(client.address)+' source_type:'+str(client.source_type)+' interest:'+str(client.interest)+' created_by:'+str(client.created_by)+' updated_by:'+str(client.updated_by)+' managers:')
    if managerList != ['']:
        for item in managerList:
            logcat.write(str(item)+' ')
    #logcat.write('\n')
    #logcat.write('-------------------')
    #logcat.write('\n')
    #logcat.close()
    contactClient = ContactClient.objects.filter(client_id=request.GET['client_id'])
    for item in contactClient:
        contact = Contact.objects.get(contact_id = item.contact_id)
        contact.delete()
        item.delete()
    client.delete()
    return JsonResponse({'success':200,'message':{}})

def check_client(request):
    clients = Client.objects.filter(customer_name = request.GET['customer_name'])
    clientsList = []
    if clients.exists():
        for item in clients:
            content = {'client_id':item.client_id}
            clientsList.append(content)
        return JsonResponse({'clientsList':clientsList,'len':clients.count()})
    else:
        return JsonResponse({'clientsList':clientsList,'len':0})

#获取用户某个时间点资产信息
def get_user_fund_time(request):
    time = request.GET['time']
    client = Client.objects.get(client_id = request.GET['client_id'])
    if client.ta_id == "":
        content = {'success':200,'type':0,'fundlist':''}
        return JsonResponse(content)
    else:
        total = accountHomeRse(client.ta_id,time)
        print '____',total['fundlist']
        content = {'success':200,'type':1,'assets':total['assets'],'totalreturn_money':total['totalreturn_money'],'totalreturn_rate':total['totalreturn_rate'],
                   'fundlist':total['fundlist']}
        return JsonResponse(content)

def send_to_ta(SoapMessage):
    url = 'https://114.255.18.179:8443/acme/services/CustomerServiceImpl?wsdl'
    client = TAClient(url)
    result = client.service.updateCustomer(json.dumps(SoapMessage))
    return result

def get_estimate_nav(request):
    beginDate = request.GET['beginDate']
    endDate = request.GET['endDate']
    riskFree = request.GET['riskFree']
    fundID = request.GET['fundID']
    type = request.GET['type']
    ta = tasver.FundDaylyNavReq()
    ta.fundid = fundID
    ta.begday = beginDate
    ta.endday = endDate
    ta.rateofreturn = str(riskFree)
    header = tasver.Header()
    header.cmd = int(type)
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.FundDaylyNavRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
        records =  json.loads(oAccountJon)
        print records
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

    excalurl = getExcal(records,int(type))
    return JsonResponse({'excalurl':excalurl,'success':200})


def get_estimate_details(beginDate,endDate,fundID):
    ta = tasver.FundDaylyNavReq()
    ta.fundid = fundID
    ta.begday = beginDate
    ta.endday = endDate
    header = tasver.Header()
    header.cmd = 113
    header.ver = 0
    header.platform = 3
    header.content = pbjson.pb2json(ta)
    headdata = pbjson.pb2json(header)

    headers = {'content-type': 'application/json'}
    r = requests.post(url,headdata,headers=headers)
    headerRes = tasver.WebRspHeader()
    headerRes.ParseFromString(r.content)
    if headerRes.errCode == 0 :
        oAccountRsp = tasver.FundDaylyNavRsp()
        oAccountRsp.ParseFromString(headerRes.content)
        oAccountJon = pbjson.pb2json(oAccountRsp)
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")
    records =  json.loads(oAccountJon)
    return records

# def getExcal(records):
#     row = [u'时间',u'基金净值',u'累计净值',u'沪深300',u'上证指数',u'创业指数','',u'基金最大回撤',u'沪深300最大回撤',u'上证指数最大回撤',u'创业板指最大回撤']
#     wb = xlwt.Workbook();
#     ws = wb.add_sheet('Sheet');

# def getExcal(date,beginDate,endDate,riskFree):
def getExcal(data,dataType):
    row = [u'时间',u'基金净值',u'累计净值',u'成立以来收益率',u'沪深300',u'上证指数',u'创业指数']
    row_left = [u'基金',u'沪深300',u'上证指数',u'创业板指',u'中证500',u'深圳成指',u'恒生指数',u'恒生国企指数']
    column = [u'收益率',u'收益率（年化）',u'夏普比率',u'索提诺比率',u'基金年化波动率',u'基金收益率下行风险',u'最大回撤',u'信息比率',u'跟踪误差']
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_RIGHT
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet')

    ws.write(0,0,u'基金名称',style)
    ws.write(0,1,data['fundname'])
    if int(dataType) == 113:
        ws.write(0,9,u'估值日期',style)
        ws.write(0,10,data['cal_day'],style)

        ws.write(0,11,u'备注',style)
        if data['motherfund']:
            if int(data['deducttype']) == 1:
                ws.write(0,12,u'母基金收益率为使用净值-1来计算的实际收益率，即提取业绩报酬后的费后收益率。其他指标为费前数据计算的指标。')
            else:
                ws.write(0,12,u'母基金收益率、其他指标均为费前收益率、费前数据计算的指标。')
        else:
            ws.write(0,12,u'子基金导出均为费后收益率和费后指标。')

    for i in range(0,len(row)):
        ws.write(2,i,row[i],style)
    # i = 1
    # for i in range(0,len(column)):
    #     ws.write(i+1,8,column[i])
    i = 3
    for item in data[u'fundnav']:
        ws.write(i,0,item['date'],style)
        ws.write(i,1,float('%.4f'%item['nav']),style)
        i = i+1
    i = 3
    for item in data[u'fundnav']:
        ws.write(i,2,float('%.4f'%item['totalnav']),style)
        i = i+1
    i = 3
    for item in data[u'fundnav']:
        ws.write(i,3,('%.2f'%(item['total_return']*100))+'%',style)
        i = i+1
    i = 3
    for item in data[u'hushen']:
        ws.write(i,4,float('%.2f'%item['nav']),style)
        i = i+1
    i = 3
    for item in data[u'shangzheng']:
        ws.write(i,5,float('%.2f'%item['nav']),style)
        i = i+1
    i = 3
    for item in data[u'gem']:
        ws.write(i,6,float('%.2f'%item['nav']),style)
        i = i+1

    if int(dataType) == 113:
        for line in range(0,6):
            if line == 0:
                item = u'指标：成立日至今'
                partData = data['pub_ret_info']
            elif line == 1:
                item = u'指标：月初至今'
                partData = data['month_ret_info']
            elif line == 2:
                item = u'指标：季初至今'
                partData = data['season_ret_info']
            elif line == 3:
                item = u'指标：年初至今'
                partData = data['year_ret_info']
            elif line == 4:
                item = u'指标：近1年收益率'
                partData = data['month12_ret_info']
            elif line == 5:
                item = u'指标：运作日至今'
                partData = data['op_ret_info']

            ws.write(2+line*12,9,item,style)
            dataList = [partData['fund'],partData['hs300'],partData['shangzheng'],partData['gem'],partData['zhongzheng'],partData['shencheng'],partData['hsi'],partData['hsgi']]

            for i in range(0,len(row_left)):
                ws.write(2+line*12,10+i,row_left[i],style)

            for j in range(0,len(column)):
                ws.write(3+line*12+j,9,column[j],style)
                for k in range(0,len(dataList)):
                    if j == 0:
                        ws.write(3+line*12+j,10+k,('%.2f'%(dataList[k]['return_rate']*100))+'%',style)
                    elif j == 1:
                        ws.write(3+line*12+j,10+k,('%.2f'%(dataList[k]['year_return_rate']*100))+'%',style)
                    elif j == 2:
                        ws.write(3+line*12+j,10+k,dataList[k]['sharp_rate'],style)
                    elif j == 3:
                        ws.write(3+line*12+j,10+k,dataList[k]['thornino_rate'],style)
                    elif j == 4:
                        ws.write(3+line*12+j,10+k,('%.2f'%(dataList[k]['year_volatility']*100))+'%',style)
                    elif j == 5:
                        ws.write(3+line*12+j,10+k,('%.2f'%(dataList[k]['down_risk']*100))+'%',style)
                    elif j == 6:
                        ws.write(3+line*12+j,10+k,('%.2f'%(dataList[k]['max_drawdown']*100))+'%',style)
                    elif j == 7:
                        ws.write(3+line*12+j,10+k,dataList[k]['information_rate'],style)
                    elif j == 8:
                        ws.write(3+line*12+j,10+k,dataList[k]['trade_error'],style)

        ws.write(75,9,u'无风险收益率',style)
        ws.write(75,10,('%.2f'%(data['pub_ret_info']['fund']['no_risk_rate']*100))+'%',style)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/excal')
    wb.save(REPORT_ROOT+'/'+'nav.xls')
    return '../static/excal'+'/'+'nav.xls'
    # wb.save(REPORT_ROOT+'/'+'nav'+beginDate+'To'+endDate+'.xls')
    # return '../static/excal'+'/'+'nav'+beginDate+'To'+endDate+'.xls'

def getDiscord(fundnav):
    navList = []
    for item in fundnav:
        if datetime.strptime(item['date'], "%Y-%m-%d").date().weekday() == 4 or judge(item['date']):
            navList.append(item['nav'])
    discordList = []
    if len(navList) == 0:
        discord = 0
    else:
        for i in range(0,len(navList)):
            temList = []
            if i == 0:
                discordList.append(0)
            else:
                for j in range(0,i):
                    result = (navList[j]-navList[i])/navList[j]
                    temList.append(result)
                discordList.append(max(temList))
        discord = max(discordList)
    if discord < 0:
        discord = 0
    return discord

def getYieldAndSharpe(fundnav,riskFree):
    navList = []
    returnList = []
    for item in fundnav:
        if datetime.strptime(item['date'], "%Y-%m-%d").date().weekday() == 4 or judge(item['date']):
            navList.append(item['nav'])
    print '------------------------------------'
    print navList
    for i in range(1,len(navList)):
        returnList.append(navList[i]/navList[i-1]-1)
    print returnList
    section_income = navList[-1]/navList[0] - 1
    print section_income
    section_len = len(navList)
    print section_len
    yield_rate = pow((1+section_income),(365/section_len))-1
    print yield_rate
    fluctuation_ratio = numpy.std(returnList) * pow(52,0.5)
    print fluctuation_ratio
    sharpe = (yield_rate-float(riskFree))/fluctuation_ratio
    print sharpe
    return {'yield':yield_rate,'sharpe':sharpe}

def judge(date):
    splited = str(date).split("-")
    day_range = calendar.monthrange(int(splited[0]), int(splited[1]))
    if splited[2] == day_range[1]:
        return True
    else:
        return False

def account_intention(request):
    return render(request,'account_intention.html')

def account_check(request):
    return render(request,'account_check.html')

def getFundsList(request):
    client = Client.objects.get(client_id = request.GET['client_id'])
    if client.ta_id == None:
        content = {'fundlist':''}
    else:
        total = accountHomeRse(client.ta_id,get_time())
        content= {'fundlist':total['fundlist']}
    return JsonResponse(content)

def getFuzzyProduct(request):
    allList = get_all_product()
    productList = []
    for item in allList:
        productList.append(item)
    return JsonResponse({'productList':productList})

def saveApply(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    clientID = request.GET['clientID']
    fundID = request.GET['fundid']
    applyType = request.GET['apply_type']
    applyDate = request.GET['apply_date']
    applyAmount = request.GET['apply_amount']
    failedType  = request.GET['failedType']
    apply = Apply(client_id=clientID,fund_id=fundID,apply_type=applyType,apply_date=applyDate,apply_amount=applyAmount,input_date=time.time(),status=1,created_by = userinfo.user_name, updated_by = userinfo.user_name)
    apply.save()
    client = Client.objects.get(client_id = clientID)
    clientAccount = ClientAccount(client_id=clientID,apply_id=apply.apply_id, bank_name = '', account_name = client.customer_name, account_no = '', status = '1',created_by = userinfo.user_name, updated_by = userinfo.user_name)
    clientAccount.save()
    accredited = Accredited.objects.get(client_id = clientID, apply_id = None)
    accredited.apply_id = apply.apply_id
    accredited.failed_type = failedType
    if failedType == '':
        accredited.status = 2
        creatContact(userinfo,clientID,apply.fund_id,apply.apply_id,3,'')
    else:
        accredited.status = 1
    accredited.save()
    createAccredited(request,accredited,False,client)
    return JsonResponse({})

def deleteApply(request):
    applyID = request.GET['applyID']
    Accredited.objects.get(apply_id = applyID).delete()
    apply = Apply.objects.get(apply_id = applyID)
    clientID = apply.client_id
    try:
        applyContact = ApplyContact.objects.get(apply_id = applyID)
        contactList = Contact.objects.filter(contact_id = applyContact.contact_id)
        for item in contactList:
            item.delete()
    except:
        pass
    apply.delete()
    return JsonResponse({'clientID':clientID})


def deleteInAccredited(request):
    imgID = request.GET['imgID']
    clientID = request.GET['clientID']
    accreditedList = Accredited.objects.filter(client_id = clientID,status =1)
    failedType = ''
    for item in accreditedList:
        typeOne = False
        typeTwo = False
        typeThree = False
        AccreditedDoc.objects.filter(accredited_id = item.accredited_id).get(document_id = imgID).delete()
        accreditedDoc = AccreditedDoc.objects.filter(accredited_id = item.accredited_id)
        client = Client.objects.get(client_id = clientID)
        if client.id_no == '' or client.id_no == None:
            failedType = failedType + '0|'
        accredited = Accredited.objects.get(accredited_id = item.accredited_id)
        if accredited.apply_id == '' or accredited.apply_id == None:
            pass
        else:
            apply = Apply.objects.get(apply_id = accredited.apply_id)
            clientType = apply.apply_type
            for item in accreditedDoc:
                document = Document.objects.using('fund_report').get(document_id = item.document_id)
                if document.document_type == '1':
                    typeOne = True
                elif document.document_type == '2':
                    if clientType == '1' and time.time() - float(document.upload_date) < 7776000:
                        typeTwo = True
                elif clientType == '2':
                    typeTwo = True
                elif document.document_type == '3':
                    if clientType == '1' and time.time() - float(document.upload_date) < 7776000:
                        typeThree = True
            if not typeOne:
                failedType = failedType + '1|'
            if not typeTwo:
                failedType = failedType + '2|'
            if not typeThree:
                failedType = failedType + '3'
            item.failed_type = failedType
            item.save()
    return JsonResponse({'success':200})

def saveInSQL(client,imgID,imgName,imgType,imgContent,userinfo):
    new_document = Document(document_name=imgName, document_type=imgType, size=len(imgContent),content=imgContent,upload_date=time.time(),created_by = userinfo.user_name, updated_by = userinfo.user_name)
    new_document.save(using='fund_report')
    accreditedList = Accredited.objects.filter(client_id = client)
    for item in accreditedList:
        accreditedDoc = AccreditedDoc.objects.filter(accredited_id = item.accredited_id)
        if imgType == '2':
            for chlid_item in accreditedDoc:
                document = Document.objects.using('fund_report').get(document_id = chlid_item.document_id)
                if document.document_type == '2':
                    documentID = chlid_item.document_id
                    AccreditedDoc.objects.filter(document_id = documentID).delete()
                    # new_accreditedDoc = AccreditedDoc(accredited_id = item.accredited_id,document_id = new_document.document_id,created_by = userinfo.user_name, updated_by = userinfo.user_name)
                    # new_accreditedDoc.save()
        if imgID == '' or imgID == '0':
            new_accreditedDoc = AccreditedDoc(accredited_id = item.accredited_id,document_id = new_document.document_id,created_by = userinfo.user_name, updated_by = userinfo.user_name)
            new_accreditedDoc.save()
        else:
            for child_item in accreditedDoc:
                if child_item.document_id == int(imgID):
                    AccreditedDoc.objects.filter(accredited_id = item.accredited_id).get(document_id = imgID).delete()
                    new_accreditedDoc = AccreditedDoc(accredited_id = item.accredited_id,document_id = new_document.document_id,created_by = userinfo.user_name, updated_by = userinfo.user_name)
                    new_accreditedDoc.save()
        failedTypeList = item.failed_type.split('|')
        newFailedType = ''
        for child_item in failedTypeList:
            if child_item != imgType and child_item != '':
                newFailedType = newFailedType + child_item + '|'
        accredited = Accredited.objects.get(accredited_id = item.accredited_id)
        if accredited.failed_type == newFailedType:
            pass
        else:
            accredited.failed_type = newFailedType
            accredited.save()
        if accredited.failed_type == '' and accredited.apply_id != None and accredited.status == '1':
            apply = Apply.objects.get(apply_id = accredited.apply_id)
            creatContact(userinfo,client,apply.fund_id,apply.apply_id,3,'')
            accredited.status = '2'
            accredited.save()

def imageUpload(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    imageContent = request.POST['imageContent']
    imgName = request.POST['imgName']
    imgID = request.POST['imgID']
    imgType = request.POST['imgType']
    clientID = request.POST['clientID']
    imgBase64 = imageContent.encode('utf-8')
    imgList = imgBase64.split('base64,')
    imgData = base64.b64decode(imgList[1])
    t = threading.Thread(target=saveInSQL, args=(clientID,imgID,imgName,imgType,imgData,userinfo,))
    t.start()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/tempfiles')
    newImg = open(REPORT_ROOT+'/'+imgName,'wb')
    newImg.write(imgData)
    newImg.close()
    return JsonResponse({'url':imgName})

def check_info(client):
    accredited = Accredited.objects.get(client_id = client,apply_id = None)
    accrediteddoc = AccreditedDoc.objects.filter(accredited_id = accredited.accredited_id)
    document1 = []
    document2 = []
    document3 = []
    for item in accrediteddoc:
        document = Document.objects.using('fund_report').get(document_id = item.document_id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/tempfiles');
        WriteFileData = open(REPORT_ROOT+'/'+str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'wb')
        # if document.document_type == '2':
        #     WriteFileData.write(base64.b64decode(document.content))
        # else:
        WriteFileData.write(document.content)
        WriteFileData.close()
        if document.document_type == '1':
            document1.append({'name':str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'id':document.document_id})
        if document.document_type == '2':
            document2.append({'name':str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'id':document.document_id})
        if document.document_type == '3':
            document3.append({'name':str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'id':document.document_id})
    return [document1,document2,document3]

def createAccredited(request,accredited,first,client):
    print '----------createAccredited1'
    try:
        userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    except:
        userinfo = UserInfo.objects.get(user_id = 1003)
    print '----------createAccredited2'
    failedType = ''
    if client.id_no == '' or client.id_no == None:
        failedType = '0|'
    if first:
        print '----------createAccredited3'
        newAccredited = Accredited(client_id = client.client_id, status=1, failed_type = failedType, created_by = userinfo.user_name, updated_by = userinfo.user_name)
        print '----------createAccredited4'
        newAccredited.save()
        print '----------createAccredited5'
    else:
        print '----------createAccredited6'
        newAccredited = Accredited(client_id = accredited.client_id, status=1, failed_type = failedType, created_by = userinfo.user_name, updated_by = userinfo.user_name)
        print '----------createAccredited7'
        newAccredited.save()
        print '----------createAccredited8'
        accrediteddoc = AccreditedDoc.objects.filter(accredited_id = accredited.accredited_id)
        for item in accrediteddoc:
            new_accreditedDoc = AccreditedDoc(accredited_id = newAccredited.accredited_id,document_id = item.document_id,created_by = userinfo.user_name, updated_by = userinfo.user_name)
            new_accreditedDoc.save()

def getApplyList(request):
    apply = Apply.objects.filter(client_id = request.GET['clientID'])
    applyList = []
    for item in apply:
        fundDetails = fund_details_chart(item.fund_id)
        fundName = fundDetails['fundname']
        applyDate = item.apply_date
        content = {'applyID':item.apply_id,'applyFundID':item.fund_id,'applyFundName':fundName,'inputDate':item.input_date,'applyType':item.apply_type,'applyAmount':item.apply_amount,'applyCount':item.apply_count,'applyDate':applyDate}
        applyList.append(content)
    return JsonResponse({'applyList':applyList})

def judgeAcc(request):
    clientType = request.GET['applyType']
    typeOne = False
    typeTwo = False
    typeThree = False
    threeMonth = False
    threeYear = False
    failedType = ''
    client = Client.objects.get(client_id = request.GET['clientID'])
    if client.id_no == '' or client.id_no == None:
        failedType = failedType + '0|'
    accredited = Accredited.objects.get(client_id = request.GET['clientID'],apply_id = None)
    accreditedDoc = AccreditedDoc.objects.filter(accredited_id = accredited.accredited_id)
    print '______________0',time.time()
    for item in accreditedDoc:
        document = Document.objects.using('fund_report').get(document_id = item.document_id)
        if document.document_type == '1':
            typeOne = True
        elif document.document_type == '2':
            threeYear = True
            if clientType == '1' and time.time() - float(document.upload_date) < 94608000:
                typeTwo = True
            elif clientType == '2' or clientType == '3':
                typeTwo = True
        elif document.document_type == '3':
            threeMonth = True
            if clientType == '1' or clientType == '2':
                print '______',clientType
                if time.time() - float(document.upload_date) < 7776000:
                    typeThree = True
                else:
                    print '______________1',time.time()
                    total = accountHomeRse(client.ta_id,get_time())
                    print '______________2',time.time()
                    if int(total['assets']) > 3000000:
                        typeThree = True
            else:
                typeThree = True
    print '______________3',time.time()
    if not typeOne:
        failedType = failedType + '1|'
    if not typeTwo:
        failedType = failedType + '2|'
    if not typeThree:
        failedType = failedType + '3'
    print failedType
    return JsonResponse({'failedType':failedType,'threeMonth':threeMonth,'threeYear':threeYear})

def account_apply(request):
    return render(request,'account_apply.html')

def account_add_apply(request):
    return render(request,'account_add_apply.html')

def account_redemption_apply(request):
    return render(request,'account_redemption_apply.html')

def applyDetails(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    apply = Apply.objects.get(apply_id = request.GET['applyID'])
    accredited = Accredited.objects.get(apply_id = request.GET['applyID'])
    fundDetails = fund_details_chart(apply.fund_id)
    fundName = fundDetails['fundname']
    content = {'applyID':apply.apply_id,'applyFundID':apply.fund_id,'applyFundName':fundName,'apply_status':apply.status,'inputDate':apply.input_date,'applyType':apply.apply_type,'applyAmount':apply.apply_amount,'applyCount':apply.apply_count,'applyDate':apply.apply_date,'failedType':accredited.failed_type,'username':userinfo.user_name,'signContractDate':apply.sign_contract_date}
    try:
        clientAccount = ClientAccount.objects.get(apply_id = apply.apply_id)
        content['bankName'] = clientAccount.bank_name
        content['bankNo'] = clientAccount.account_no
        content['baseCheck'] = apply.info_flag
        content['cardCheck'] = apply.idtype_flag
        content['testCheck'] = apply.questionnaire_flag
        content['assetCheck'] = apply.asset_flag
        content['contractCheck'] = apply.contract_flag
        content['applyCheck'] = apply.applytab_flag
    except:
        pass
    content['account_date'] = apply.account_date
    content['silence_date'] = apply.silence_date
    content['HF_date'] = apply.HF_date
    content['complete_date'] = apply.complete_date
    try:
        applyContactList = ApplyContact.objects.filter(apply_id = apply.apply_id)
        for item in applyContactList:
            contact = Contact.objects.get(contact_id = item.contact_id)
            if contact.contact_type == "2":
                content['complete_per'] = contact.updated_by
    except:
        content['complete_per'] = ''
    return JsonResponse(content)

def fund_details_chart(fundID):
    ta = tasver.WebFundDetailReq()
    ta.fundid = fundID
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
        return detailInfo
    else :
        print "ErrCode:"
        print headerRes.errCode
        print "ErrMsg:"
        print headerRes.errMsg.encode("utf-8")

def newContent(request):
    user = UserInfo.objects.get(user_id = request.session['user_id'])
    contact = Contact(contact_date='2016-09-20 09:00',contact_user_id=user.user_id,contact_detail='打印寄送合同',contact_record='',task_status=1,contact_type=1,created_by=user.user_name,updated_by=user.user_name)
    contact.save()
    contactClient = ContactClient(contact_id=contact.contact_id,client_id=request.GET['clientID'],created_by=user.user_name,updated_by=user.user_name)
    contactClient.save()

def infoAboutAuestionnaire(request):
    clientID = unescape(request.GET['clientID'])
    print clientID,'---------------------------'
    client = Client.objects.get(id_no = clientID)
    realname = client.customer_name
    idtype = client.id_type
    idno = client.id_no
    email = client.customer_email
    if len(idno) > 8:
        idno = idno.replace(idno[6:],"******")
    try:
        mobile = client.mobile
        if len(mobile) > 8:
            mobile = mobile.replace(mobile[3:7],"****")
    except:
        moblie = ''
    print '-------------',email
    emailExist = '1'
    if email is None:
        emailExist = '0'
    elif len(email) < 3:
        emailExist = '0'
    content = {"realname":realname,'idtype':idtype,'idno':idno,'mobile':mobile,'emailExist':emailExist}
    return JsonResponse(content)

#存储调查问卷相关信息（个人）
def ResultAboutAuestionnaire(request):
    clientSubArray = request.POST['subQaArray'].split('||')
    clientArray = request.POST['clientArray'].split('||')
    clientID = unescape(request.POST['clientID'])
    print '---------------------------oooooo--------------',clientID
    totalPoint = 0
    for point in (request.POST['point']).split('.'):
        totalPoint += int(point)
    try:
        client = Client.objects.get(id_no = clientID)
        client.risk_type = request.POST['point']
        client.save()
    except:
        pass
    request.session['totalPoint'] = totalPoint
    try:
        t = threading.Thread(target=createAndStorePDF,args=(request, clientID, clientSubArray, clientArray, request.POST['point']))
        t.start()
    except Exception, e:
        try:
            f = open("except.txt", 'a')
            f.write('....')
            f.write(time.time())
            f.write('....')
            f.write(str(Exception))
            f.write('....')
            f.write(str(e))
            f.write('\r\n')
            f.close()
            t = threading.Thread(target=createAndStorePDF,args=(request, clientID, clientSubArray, clientArray, request.POST['point']))
            t.start()
        except:
            t = threading.Thread(target=createAndStorePDF,args=(request, clientID, clientSubArray, clientArray, request.POST['point']))
            t.start()

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

    if int((request.POST['point']).split('.')[11]) == 1:
        level = 1

    print '-------------,'+'&level=C'+str(level)

    user = UserInfo.objects.get(user_id = 1003)
    contact = Contact(contact_date=str(time.strftime("%Y-%m-%d")),contact_user_id = 1001,contact_detail='该用户已完成风险测评，得分为'+str(totalPoint)+'，风险等级为C'+str(level)+'，客户尚未完成风险披露。',contact_record='',task_status=2,contact_type=10,created_by=user.user_name,updated_by=user.user_name)
    contact.save()
    contactClient = ContactClient(contact_id=contact.contact_id,client_id=client.client_id,created_by=user.user_name,updated_by=user.user_name)
    contactClient.save()

    if client.customer_type == '1':
        return JsonResponse({'url':'../riskEvaluation_result?clientID='+request.POST['clientID']+'&result='+str(totalPoint)+'&type=1'+'&level=C'+str(level)})
    else:
        return JsonResponse({'url':'../riskEvaluation_result?clientID='+request.POST['clientID']+'&result='+str(totalPoint)+'&type=2'+'&level=C'+str(level)})

#存储调查问卷相关信息（机构）
def ResultAboutQuestionnaire(request):
    print '---------------------0'
    print request.POST['point']
    clientArray = request.POST['clientArray'].split('||')
    print '---------------------1'
    print clientArray
    print '---------------------2'
    totalPoint = 0
    print request.POST['point']
    for point in (request.POST['point']).split('.'):
        totalPoint += int(point)

    clientID = unescape(request.POST['clientID'])
    print '-------------',clientID
    totalPoint = 0
    for point in (request.POST['point']).split('.'):
        totalPoint += int(point)
    try:
        client = Client.objects.get(id_no = clientID)
        client.risk_type = request.POST['point']
        client.save()
    except:
        pass
    print '------------',totalPoint
    # client = Client.objects.get(id_no = clientID)
    # client.risk_type = request.POST['point']
    # client.save()
    request.session['totalPoint'] = totalPoint

    t = threading.Thread(target=createAndStoreOrgPDF,args=(request, clientID, clientArray, request.POST['point']))
    t.start()

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

    print 'point','---------------',int((request.POST['point']).split('.')[16])

    if int((request.POST['point']).split('.')[16]) == 1:
        level = 1

    user = UserInfo.objects.get(user_id = 1003)
    contact = Contact(contact_date=str(time.strftime("%Y-%m-%d")),contact_user_id = 1001,contact_detail='该用户已完成风险测评，得分为'+str(totalPoint)+'，风险等级为C'+str(level)+'，客户尚未完成风险披露。',contact_record='',task_status=2,contact_type=10,created_by=user.user_name,updated_by=user.user_name)
    contact.save()
    contactClient = ContactClient(contact_id=contact.contact_id,client_id=client.client_id,created_by=user.user_name,updated_by=user.user_name)
    contactClient.save()

    if client.customer_type == '1':
        return JsonResponse({'url':'../riskEvaluation_result?clientID='+request.POST['clientID']+'&type=1'+'&result='+str(totalPoint)+'&level=C'+str(level)})
    else:
        return JsonResponse({'url':'../riskEvaluation_result?clientID='+request.POST['clientID']+'&type=2'+'&result='+str(totalPoint)+'&level=C'+str(level)})

def createAndStorePDF(request, clientID, clientSubArray, clientArray, totalPoint):
    client = Client.objects.get(id_no = clientID)
    timeTampName = creatNewPDF(client, clientSubArray, clientArray, totalPoint)
    file = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gaoyicrm/static/tempfiles/'+ timeTampName),'rb')              #二进制方式打开图文件
    fileRead = file.read()
    file.close()
    try:
        userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    except:
        userinfo = UserInfo.objects.get(user_id = 1003)

    saveInSQL(client.client_id,'0',str(client.client_id)+'_'+str(time.time())+'.pdf','2',fileRead, userinfo)
    return JsonResponse({})

def createAndStoreOrgPDF(request, clientID, clientArray, totalPoint):
    client = Client.objects.get(id_no = clientID)
    timeTampName = createOrgPDF(client, clientArray, totalPoint)
    file = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gaoyicrm/static/tempfiles/'+ timeTampName),'rb')              #二进制方式打开图文件
    fileRead = file.read()
    file.close()
    try:
        userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    except:
        userinfo = UserInfo.objects.get(user_id = 1003)

    saveInSQL(client.client_id,'0',str(client.client_id)+'_'+str(time.time())+'.pdf','2',fileRead, userinfo)
    return JsonResponse({})

# def createPDF(request,qaArray,clientID,totalPoint=0,output="client_report.pdf",):
#     now = datetime.today()
#     date = now.strftime('%Y-%m-%d')
#     c = canvas.Canvas(output)
#     client = Client.objects.get(client_id = clientID)
#     if client.customer_type == '1':
#         DrawCanvasPerson1(c,clientID,date,qaArray[0:20])
#         c.showPage()
#         DrawCanvasPerson2(c,qaArray[20:61])
#         c.showPage()
#         DrawCanvasPerson3(c,qaArray[61:],totalPoint)
#         c.showPage()
#         c.save()
#     else:
#         DrawCanvasOrg1(c,clientID,date,qaArray[0:18])
#         c.showPage()
#         DrawCanvasOrg2(c,qaArray[18:])
#         c.showPage()
#         DrawCanvasOrg3(c,totalPoint)
#         c.showPage()
#         c.save()
#     file = open(r'client_report.pdf','rb')              #二进制方式打开图文件
#     fileRead = file.read()
#     file.close()
#     userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
#     saveInSQL(clientID,'0',str(clientID)+'_'+str(time.time())+'.pdf','2', fileRead, userinfo)

def creatContact(userinfo,clientID,fundID,applyID,type,CapitalDate):
    userID = userinfo.user_id
    userName = userinfo.user_name
    fundDetails = fund_details_chart(fundID)
    apply = Apply.objects.get(apply_id = applyID)
    detail = '打印材料连同《'+fundDetails['fundname']+'》合同寄出并收回！'
    if apply.apply_type == '2':
        detail = '打印资产证明和《'+fundDetails['fundname']+'》的直销申请表寄出并收回'
    elif apply.apply_type == '3':
        detail = '打印《'+fundDetails['fundname']+'》的直销申请表寄出并收回'
    state = '2'
    if type == 3:
        contact = Contact(contact_date=fundDetails['nextopenday'],contact_user_id=1001,contact_detail=detail,contact_record='',task_status=state,contact_type=3,note=str(fundID)+'.'+str(applyID)+'.'+str(apply.apply_type),created_by=userID,updated_by=userID)
    elif type == 2:
        newDate = DTtime.datetime.strptime(str(CapitalDate),'%Y-%m-%d %H:%M:%S')
        tomorrow = newDate + DTtime.timedelta(days=1)
        contact = Contact(contact_date=fundDetails['nextopenday'],contact_user_id=1000,contact_detail='请于'+str(tomorrow)+'后完成《'+fundDetails['fundname']+'》的静默回访',contact_record='',task_status=state,contact_type=2,note=str(fundID)+'.'+str(applyID)+'.'+str(apply.apply_type),created_by=userID,updated_by=userID)
    contact.save()
    applyContact = ApplyContact(apply_id = applyID, contact_id = contact.contact_id ,created_by=userName,updated_by=userName)
    applyContact.save()
    contactClient = ContactClient(contact_id=contact.contact_id,client_id=clientID,created_by=userName,updated_by=userName)
    contactClient.save()

def save_contact_record(request):
    contact = Contact.objects.get(contact_id=request.GET['contact_id'])
    user = UserInfo.objects.get(user_id = request.session['user_id'])
    contact.contact_record = request.GET['contact_record']
    contact.record_date = time.strftime('%Y-%m-%d %H:%M:%S')
    contact.task_status = 1
    contact.updated_by = user.user_name
    contact.save()
    try:
        applyContact = ApplyContact.objects.get(contact_id = contact.contact_id)
        apply = Apply.objects.get(apply_id = applyContact.apply_id)
        apply.status = 3
        apply.HF_date = time.strftime('%Y-%m-%d %H:%M:%S')
        apply.save()
        updateApplyContact(apply)
    except:
        pass
    contactClient = ContactClient.objects.get(contact_id = contact.contact_id)
    logcat = open("logcat.txt", 'a')
    logcat.write('Time:'+str(get_time_details())+'  '+'User:'+str(user.user_name)+'\n')
    logcat.write('Action:Complete a contact with ID '+str(contact.contact_id)+' about client '+str(contactClient.client_id)+'\n')
    logcat.write('Details:contact_date:'+str(contact.contact_date)+' contact_user_id:'+str(contact.contact_user_id)+' contact_detail:'+str(contact.contact_detail)+' contact_record:'+str(contact.contact_record)+' task_status:'+str(contact.task_status)+' contact_type:'+str(contact.contact_type)+' contact_user_id:'+str(contact.contact_user_id)+' created_by:'+str(contact.created_by)+' updated_by:'+str(contact.updated_by))
    logcat.write('\n')
    logcat.write('-------------------')
    logcat.write('\n')
    logcat.close()
    contactClientList = ContactClient.objects.filter(client_id = request.GET['client_id'])
    contactList = []
    for item in contactClientList:
        contact = Contact.objects.get(contact_id=item.contact_id)
        user = UserInfo.objects.get(user_id = contact.contact_user_id)
        content = {'contact_id':contact.contact_id,'task_date':contact.contact_date,'contact_user':user.user_name,'contact_detail':contact.contact_detail,'contact_record':contact.contact_record,'task_status':contact.task_status}
        if contact.task_status == '1':
            content['task_date'] = contact.record_date
        contactList.insert(0,content)
    return JsonResponse({'success':200,'contactList':contactList,'contactList_len':len(contactList)})

def updateClientAccount(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    applyAmount = request.GET['applyAmount']
    userBankName = request.GET['userBankName']
    userBankNo = request.GET['userBankNo']
    userTime  = request.GET['userTime']
    moneyTime = request.GET['moneyTime']
    baseCheck = request.GET['baseCheck']
    cardCheck = request.GET['cardCheck']
    testCheck = request.GET['testCheck']
    assetCheck = request.GET['assetCheck']
    contractCheck = request.GET['contractCheck']
    applyCheck = request.GET['applyCheck']
    applyID = request.GET['applyID']
    apply = Apply.objects.get(apply_id = applyID)
    client = Client.objects.get(client_id = apply.client_id)
    if baseCheck == 'true':
        apply.info_flag = '1'
    else:
        apply.info_flag = '0'
    if cardCheck == 'true':
        apply.idtype_flag = '1'
    else:
        apply.idtype_flag = '0'
    if testCheck == 'true':
        apply.questionnaire_flag = '1'
    else:
        apply.questionnaire_flag = '0'
    if assetCheck == 'true':
        apply.asset_flag = '1'
    else:
        apply.asset_flag = '0'
    if contractCheck == 'true':
        apply.contract_flag = '1'
    else:
        apply.contract_flag = '0'
    if applyCheck == 'true':
        apply.applytab_flag = '1'
    else:
        apply.applytab_flag = '0'
    if moneyTime != '':
        if apply.account_date == '':
            apply.account_date = moneyTime
            apply.silence_date = DTtime.datetime.strptime(moneyTime + " 18:00:00", '%Y-%m-%d %H:%M:%S') + DTtime.timedelta(days=1)
            creatContact(userinfo,apply.client_id,apply.fund_id,apply.apply_id,2,moneyTime + " 18:00:00")
    apply.sign_contract_date = userTime
    apply.apply_amount = applyAmount
    apply.save()
    if apply.status == '3' or apply.apply_type == '3':
        updateApplyContact(apply)
    clientAccount = ClientAccount.objects.get(apply_id = applyID)
    clientAccount.bank_name = userBankName
    clientAccount.account_name = client.customer_name
    clientAccount.account_no = userBankNo
    clientAccount.save()
    capitalMatch(request)
    return JsonResponse({'clientID':client.client_id})

#根据用户预约信息判断是否完成待收取合同
def updateApplyContact(apply):
    if apply.apply_type == '1':
        if apply.sign_contract_date != '' and apply.info_flag == '1' and apply.idtype_flag == '1' and apply.questionnaire_flag == '1' and apply.asset_flag == '1' and apply.contract_flag == '1' and apply.applytab_flag == '1':
            applyContact = ApplyContact.objects.filter(apply_id = apply.apply_id)
            for item in applyContact:
                contact = Contact.objects.get(contact_id = item.contact_id)
                if contact.contact_type == '3':
                    contact.task_status = '1'
                    contact.record_date = time.strftime('%Y-%m-%d %H:%M:%S')
                    contact.save()
                    apply.status = '4'
                    apply.save()
    elif apply.apply_type == '2':
        if apply.asset_flag == '1' and apply.applytab_flag == '1':
            applyContact = ApplyContact.objects.filter(apply_id = apply.apply_id)
            for item in applyContact:
                contact = Contact.objects.get(contact_id = item.contact_id)
                if contact.contact_type == '3':
                    contact.task_status = '1'
                    contact.record_date = time.strftime('%Y-%m-%d %H:%M:%S')
                    contact.save()
                    apply.status = '4'
                    apply.save()
    elif apply.apply_type == '3':
        clientAccount = ClientAccount.objects.get(apply_id = apply.apply_id)
        if apply.applytab_flag == '1' and clientAccount.bank_name != '' and clientAccount.account_no != '':
            applyContact = ApplyContact.objects.filter(apply_id = apply.apply_id)
            for item in applyContact:
                contact = Contact.objects.get(contact_id = item.contact_id)
                contact.task_status = '1'
                contact.record_date = time.strftime('%Y-%m-%d %H:%M:%S')
                contact.save()
                apply.status = '4'
                apply.save()

from excelparser import XlsToMysql
def xlsHandle(request):
    xlsName = request.POST['xlsName']
    xlsContent = request.POST['xlsContent']
    xlsBase64 = xlsContent.encode('utf-8')
    xlsList = xlsBase64.split('base64,')
    xlsData = base64.b64decode(xlsList[1])
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/tempfiles');
    newImg = open(REPORT_ROOT+'/'+xlsName,'wb')
    newImg.write(xlsData)
    newImg.close()
    try:
        XlsToMysql(REPORT_ROOT+'/'+xlsName)
        capitalMatch(request)
        return JsonResponse({'success':200})
    except:
        return JsonResponse({'success':403})

def capitalMatch(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    capitalList = Capital.objects.filter(status = 1)
    clientAccountList = ClientAccount.objects.all()
    for item1 in capitalList:
        payeeAccountNo = item1.payee_account_no
        payeeAccountName = item1.payee_account_name
        payCreditSum = item1.credit_sum
        for item2 in clientAccountList:
            print payeeAccountNo,item2.account_no,payeeAccountName,item2.account_name
            if payeeAccountNo == item2.account_no and payeeAccountName == item2.account_name:
                applyID = item2.apply_id
                apply = Apply.objects.get(apply_id = applyID)
                if apply.apply_amount == payCreditSum and apply.fund_id == item1.fund_id:
                    item1.status = 2
                    item1.save()
                    applyCapital = ApplyCapital(apply_id = apply.apply_id,capital_id = item1.capital_id,created_by = 'CRM', updated_by = 'CRM')
                    applyCapital.save()
                    apply.status = 2
                    apply.account_date = item1.capital_date
                    apply.silence_date = item1.capital_date
                    apply.save()
                    creatContact(userinfo,apply.client_id,apply.fund_id,apply.apply_id,2,item1.capital_date)


def getClientCheck(request):
    documentList = check_info(request.GET['clientID'])
    client = Client.objects.get(client_id = request.GET['clientID'])
    pointList = client.risk_type
    clientRisk = 0
    for point in pointList.split('.'):
        clientRisk += int(point)
    print '------------clientRisk',clientRisk,client.customer_type
    if int(client.customer_type) == 0:
        if clientRisk <= 58:
            level = 1
        elif clientRisk <= 67:
            level = 2
        elif clientRisk <= 76:
            level = 3
        elif clientRisk <= 85:
            level = 4
        else:
            level = 5
        if int(client.risk_type.split('.')[16]) == 1:
            level = 1
    else:
        if clientRisk <= 32:
            level = 1
        elif clientRisk <= 38:
            level = 2
        elif clientRisk <= 43:
            level = 3
        elif clientRisk <= 48:
            level = 4
        else:
            level = 5
        if int(client.risk_type.split('.')[11]) == 1:
            level = 1
    print '------------clientRisk',clientRisk,client.customer_type,level
    return JsonResponse({'documentList':documentList,'clientRisk':clientRisk,'level':level})

def getClientDoc(request):
    try:
        fundAndApply = request.GET['fundAndApply']
        applyID = fundAndApply.split('.')[1]
        documentList = []
        apply = Apply.objects.get(apply_id = applyID)
        clientAccount = ClientAccount.objects.get(apply_id = apply.apply_id)
        client = Client.objects.get(client_id = clientAccount.client_id)
        accredited = Accredited.objects.get(apply_id = applyID)
        accreditedDocList = AccreditedDoc.objects.filter(accredited_id = accredited.accredited_id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/tempfiles')

        if apply.apply_type == '1':
            #获取空白的信息表,自然人为1机构为2
            if client.customer_type == '1':
                WriteFileData = open(REPORT_ROOT+'/1_|_自然人客户信息表.pdf','wb')
                WriteFileData.write(Document.objects.using('fund_report').get(document_id = 1).content)
                documentList.append({'name':'1_|_自然人客户信息表.pdf','id':1})
            else:
                WriteFileData = open(REPORT_ROOT+'/2_|_机构客户信息表.pdf','wb')
                WriteFileData.write(Document.objects.using('fund_report').get(document_id = 2).content)
                documentList.append({'name':'2_|_机构客户信息表.pdf','id':1})
            WriteFileData.close()
        else :
            WriteFileData = open(REPORT_ROOT+'/3_|_直销申请表.pdf','wb')
            WriteFileData.write(Document.objects.using('fund_report').get(document_id = 3).content)
            documentList.append({'name':'3_|_直销申请表.pdf','id':1})
            WriteFileData.close()
        if apply.apply_type != '3':
            for item in accreditedDocList:
                document = Document.objects.using('fund_report').get(document_id = item.document_id)
                if document.document_type != '3':
                    if apply.apply_type == '1':
                        WriteFileData = open(REPORT_ROOT+'/'+str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'wb')
                        WriteFileData.write(document.content)
                        WriteFileData.close()
                        documentList.append({'name':str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'id':document.document_id})
                else:
                    WriteFileData = open(REPORT_ROOT+'/'+str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'wb')
                    WriteFileData.write(document.content)
                    WriteFileData.close()
                    documentList.append({'name':str(document.document_id)+'_|_'+(document.document_name).encode('utf-8'),'id':document.document_id})
        return JsonResponse({'documentList':documentList})
    except:
        return JsonResponse({'documentList':'403'})

from sendmail2 import sendinfomail
def sentInfoMail(request):
    clientID = request.GET['clientID']
    client = Client.objects.get(client_id = clientID)
    content = '尊敬的客户，您好！\n我们收到了您的投资意向。\n'
    failedTypeList = request.GET['failedType'].split('|')
    for item in failedTypeList:
        if item == '1':
            content = content+'请您提供身份证明信息，\n'
        if item == '3':
            content = content+'请您提供资产证明信息，\n'
        if item == '2':
            if client.customer_type == '1':
                content = content+'请您前往如下地址进行风险测试：https://crm.gyasset.com/questionnaire/clientclient='+clientID+'\n'
            else:
                content = content+'请您前往如下地址进行风险测试：https://crm.gyasset.com/org_questionnaire/clientclient='+clientID+'\n'
    if content == '您好！\n':
        content = '合同已经寄出，请注意查收！'
    t = threading.Thread(target=sendinfomail, args=('高毅资产客户信息补充邀请',content,client.customer_email,))
    t.start()
    t.join()
    return JsonResponse({'success':200})
    # if sendinfomail(content,client.customer_email):
    #     return JsonResponse({'success':200})
    # else:
    #     return JsonResponse({'success':403})

def getTotalApplyList(request):
    fundID = request.GET['fundID']
    type = request.GET['type']
    status = request.GET['status']
    if fundID == '9':
        applyList = Apply.objects.all()
    else:
        applyList = Apply.objects.filter(fund_id = fundID)

    if applyList == []:
        return JsonResponse({})

    if type == '9':
        pass
    else:
        if type == '1':
            type = [1,2]
        else:
            type = [int(type)]
        applyList = applyList.filter(apply_type__in = type)

    if applyList == []:
        return JsonResponse({})

    if status == '9':
        pass
    else:
        if status == '1':
            status = [1,2,3]
        else:
            status = [int(status)]
        print status
        applyList = applyList.filter(status__in = status)

    if applyList == []:
        return JsonResponse({})
    sendApplyList = []
    for item in applyList:
        clientAccount = ClientAccount.objects.get(apply_id = item.apply_id)
        try:
            applyCapital = ApplyCapital.objects.get(apply_id = item.apply_id)
            capitalID = applyCapital.capital_id
        except:
            capitalID = ''
        fundDetails = fund_details_chart(item.fund_id)
        fundName = fundDetails['fundname']
        nextOpenDay = item.apply_date
        content = {'applyID':item.apply_id,'clientName':clientAccount.account_name,'applyType':item.apply_type,'applyStatus':item.status,'fundName':fundName,'fundOpenDay':nextOpenDay,
                   'applyAmount':item.apply_amount,'applyCount':item.apply_count,'bankName':clientAccount.bank_name,'bankNo':clientAccount.account_no,'contractFlag':item.contract_flag,
                   'infoFlag':item.info_flag,'riskFlag':item.risk_flag,'questionnaireFlag':item.questionnaire_flag,'assetFlag':item.asset_flag,'signContractDate':item.sign_contract_date,'accountDate':item.account_date,
                   'capitalID':capitalID,'silenceDate':item.silence_date,'HFDate':item.HF_date,'updatedBy':item.updated_by,
                   }
        sendApplyList.append(content)
    return JsonResponse({'sendApplyList':sendApplyList})

from exportmsg import *
def exportMsg(request):
    fundID = request.GET['fundID']
    type = request.GET['type']
    # status = request.GET['status']
    if fundID == '9':
        applyList = Apply.objects.all()
    else:
        applyList = Apply.objects.filter(fund_id = fundID)

    if applyList == []:
        return JsonResponse({})

    if type == '9':
        pass
    else:
        if type == '1':
            type = [1,2]
        else:
            type = [int(type)]
        applyList = applyList.filter(apply_type__in = type)

    if applyList == []:
        return JsonResponse({})
    # if status == '9':
    #     pass
    # else:
    #     if status == '1':
    #         status = [1,2,3]
    #     else:
    #         status = [int(status)]
    #     print status
    applyList = applyList.filter(status__in = '4')

    if applyList == []:
        return JsonResponse({})
    GuojinList = []
    GuoxinList = []
    CMBList = []
    CMSList = []
    CITICList = []
    Guojin = False
    Guoxin = False
    CMB = False
    CMS = False
    CITIC = False
    for item in applyList:
        clientAccount = ClientAccount.objects.get(apply_id = item.apply_id)

        fundDetails = fund_details_chart(item.fund_id)
        fundName = fundDetails['fundname']
        client = Client.objects.get(client_id = clientAccount.client_id)

        oMsg = ExportInfo()
        oMsg.fundname = fundName
        oMsg.fundcode = item.fund_id
        oMsg.customertype  = client.customer_type
        oMsg.applydate = time.strftime("%Y-%m-%d", time.localtime(float(item.input_date)))
        oMsg.customername = client.customer_name
        oMsg.idtype = client.id_type
        oMsg.idno = client.id_no
        oMsg.bank = clientAccount.bank_name
        oMsg.bankname = clientAccount.bank_name
        oMsg.bankaccount = clientAccount.account_no
        oMsg.zipcode = ''
        oMsg.mobile = client.mobile
        oMsg.address = client.address
        oMsg.money = item.apply_amount
        oMsg.applymoney = item.apply_amount
        oMsg.applytype = item.apply_type
        oMsg.shuhui_all = True
        oMsg.bankaccountname = client.customer_name
        oMsg.jingban_name = client.customer_name
        oMsg.jingban_idtype = client.customer_type
        oMsg.jingban_idno = client.id_no
        oMsg.sheng = client.province
        oMsg.shi = client.city
        oMsg.shuhui_shares = ''
        oMsg.faren_name = client.customer_name
        oMsg.sex = client.sex
        print item.account_date
        oMsg.daozhang_date = item.account_date
        print oMsg.fundname
        if u'国鹭1号' in oMsg.fundname or u'邻山1号' in oMsg.fundname or u'晓峰明远' in oMsg.fundname:
            GuoxinList.append(oMsg)
            Guoxin = True
        if u'晓峰2号' in oMsg.fundname or u'世宏1号' in oMsg.fundname or u'利伟精选唯实' in oMsg.fundname:
            CMSList.append(oMsg)
            CMS = True
        if u'晓峰1号' in oMsg.fundname:
            CITICList.append(oMsg)
            CITIC = True
        if u'庆瑞3号' in oMsg.fundname:
            GuojinList.append(oMsg)
            Guojin = True
        if u'高毅FOF' in oMsg.fundname or u'核心价值1期' in oMsg.fundname:
            CMBList.append(oMsg)
            CMB = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT1 = os.path.join(BASE_DIR, 'gaoyicrm/static/xls_models/');
    REPORT_ROOT2 = os.path.join(BASE_DIR, 'gaoyicrm/static/xls_output/');
    newUrlList = []
    if Guoxin:
        ExportToGuoXin(REPORT_ROOT1+'/'+'guoxin.xls',REPORT_ROOT2+'/'+'guoxin.xls',GuoxinList)
        newUrlList.append('../static/xls_output/guoxin.xls')
    if CMS:
        ExportToCMS(REPORT_ROOT1+'/'+'zhaozheng_shengou.xls',REPORT_ROOT1+'/'+'zhaozheng_shuhui.xls',REPORT_ROOT2+'/'+'zhaozheng_shengou.xls',REPORT_ROOT2+'/'+'zhaozheng_shuhui.xls',CMSList)
        newUrlList.append('../static/xls_output/zhaozheng_shengou.xls')
    if CMB:
        ExportToCMB(REPORT_ROOT1+'/'+'zhaohang.xls',REPORT_ROOT2+'/'+'zhaohang.xls',CMBList)
        newUrlList.append('../static/xls_output/zhaohang.xls')
    if CITIC:
        ExportToCITIC(REPORT_ROOT1+'/'+'zhongxin.xls',REPORT_ROOT2+'/'+'zhongxin.xls',CITICList)
        newUrlList.append('../static/xls_output/zhongxin.xls')
    if Guojin:
        ExportToGuojin(REPORT_ROOT1+'/'+'guojin.xls',REPORT_ROOT2+'/'+'guojin.xls',GuojinList)
        newUrlList.append('../static/xls_output/guojin.xls')
    return JsonResponse({'newUrl':newUrlList})

def getAvailableShares(request):
    client = Client.objects.get(client_id = request.GET['clientID'])
    tradeList = get_records(client.ta_id)
    for item in tradeList['recordsList']:
        print item['bneedalltradeid']
        print item['tradeid']
        # print datetime.strptime(str(item['opday']), "%Y-%m-%d").date()
        # print time.strftime("%Y-%m-%d", item['opday']*1000)

        print time.strftime('%Y-%m-%d',time.localtime(item['opday']))
        print '_______________1'
        # url = 'http://101.200.242.103:32066/efundNew/services/CustomerServiceImpl?WSDL'
        # url = 'http://101.200.242.103:32066/efundNew/services/CustomerServiceImpl?wsdl'
        # print '_______________2'
        # client = TAClient(url)
        # print client
        print '_______________3'

        client = TAClient('http://101.200.242.103:32066/efundNew/services/CustomerServiceImpl?wsdl')
        print client

        SoapMessage = {"tradeid":'7bae2512663543a3ba1e00ba3eea5563',"querydate":"2016-03-01"}
        result = client.service.calRedeemDateAndCount(json.dumps(SoapMessage))

    return JsonResponse({})

def changeRiskType(request):
    clientID = request.GET['clientID']
    riskType = request.GET['riskType']
    client = Client.objects.get(client_id = clientID)
    client.risk_type = riskType
    client.save()
    return JsonResponse({'success':'200'})

def checkBaseInfo(request):
    apply = Apply.objects.get(apply_id = request.GET['applyID'])
    client = Client.objects.get(client_id = apply.client_id)
    if client.customer_type == '1':
        if client.id_no == None or client.id_no == '' or client.birthday == None or client.birthday == '' or client.nationality == None or client.nationality == '' or client.education == None or client.education == '' or client.occupation == None or client.occupation == '':
            return JsonResponse({'success':'404','clientID':client.client_id,'clientType':'1'})
        else:
            return JsonResponse({'success':'200'})
    else:
        if client.controller == None or client.controller == '' or client.id_no == None or client.id_no == '' or client.valid_begin == None or client.valid_begin == '' or client.valid_end == None or client.valid_end == '' or client.address == None or client.address == '':
            return JsonResponse({'success':'404','clientID':client.client_id,'clientType':'0'})
        else:
            return JsonResponse({'success':'200'})

def riskEnsure(request):
    id_no = request.GET['id_no']
    client = Client.objects.get(id_no = id_no)
    contactClientList = ContactClient.objects.filter(client_id=client.client_id)

    for contactClient in contactClientList:
        try:
            contact = Contact.objects.get(contact_id = contactClient.contact_id ,contact_type = 10 ,task_status = 2)
            contact.task_status = 1
            contact.record_date = str(time.strftime("%Y-%m-%d"))
            contact.contact_record = '用户已完成风险披露'
            contact.save()
        except:
            pass

    totalPoint = 0
    for point in client.risk_type.split('.'):
        totalPoint += int(point)

    if client.customer_type == '0':
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

        if int(client.risk_type.split('.')[16]) == 1:
            level = 1
    else:
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

        if int(client.risk_type.split('.')[11]) == 1:
            level = 1

    content = '<p>尊敬的'+client.customer_name+'先生（女士）:</p>'
    content = content + '<p>您好!恭喜您已完成投资者适当性匹配环节！</p>'
    content = content + '<p>风险评估结果如下：</p>'
    content = content + '<p>您/贵机构希望投资的基金产品风险等级为R3，您/贵机构的风险承受能力为：C'+str(level)+'，高（等）于我司产品风险等级。依据我司的投资者与产品、服务风险等级匹配规则，确认您/贵机构的风险承受能力等级与我司（产品、服务风险等级）相匹配。</p>'
    content = content + '<p style="color:red"><B>若您确认以下事项，请邮件回复“确认”即可。</B></p>'
    content = content + '<p>1.本邮件收件人为本人/机构。</p><p>2.本人/机构承诺本次投资行为是为本人/机构购买本私募投资基金。</p><p>3.本人/机构已充分了解并谨慎评估自身风险承受能力，自愿自行承担投资本私募投资基金所面临的风险。</p>' \
                        '<p>4.本人/机构知晓，基金管理人、基金销售机构、基金托管人及相关机构不对基金财产的收益状况作出任何承诺或担保。知悉本基金具有一定的投资风险，管理人不保证最低收益或基金本金不受损失。</p>' \
                        '<p>5.知悉在锁定期内不得赎回，不可以在非开放期违约赎回。</p><p>6.若本人/机构提供的信息发生任何重大变化，本人/机构将及时书面通知你公司。</p>'

    t = threading.Thread(target=sendinfomail, args=('邮件标题：高毅资产投资者适当性匹配-'+client.customer_name,content,client.customer_email,))
    t.start()
    t.join()

    user = UserInfo.objects.get(user_id = 1003)
    contact = Contact(contact_date=str(time.strftime("%Y-%m-%d")),contact_user_id = 1001,contact_detail='该用户已完成风险测试问卷，得分为'+str(totalPoint)+'分，风险等级为C'+str(level)+'。用户已完成风险揭示书确认，并已发送确认邮件，等待客户回复。',contact_record='',task_status=2,contact_type=10,created_by=user.user_name,updated_by=user.user_name)
    contact.save()
    contactClient = ContactClient(contact_id=contact.contact_id,client_id=client.client_id,created_by=user.user_name,updated_by=user.user_name)
    contactClient.save()
    return JsonResponse({})

# 字符串转义函数
# def fromCharCode(a, *b):
#     return unichr(a % 65536) + ''.join([unichr(i % 65536) for i in b])

# 解密函数 escape为加密过后的值
# 返回加密前的原始值
def unescape(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
        return base64.decodestring(data)
    return base64.decodestring(data)
    # code = fromCharCode(int(ord(escape[0])) - len(escape))
    # for i in range(1, len(escape)):
    #     code += fromCharCode(int(ord(escape[i])) - int(ord(code[i - 1])))
    # return code
