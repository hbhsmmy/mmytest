# -*- coding: utf-8 -*-
from models import Client,UserInfo,Contact,ContactClient,Message,UserRole,Dictionary,ApplyContact,Apply,Documentscan,TradeDocument,TradeScan
from utils import get_time_details
from django.http import JsonResponse
from django.core.paginator import Paginator
import operator,time,base64
import threading,os
from django.shortcuts import render_to_response

import time
def sleepRequest(request):
    print "this will sleep for 3 seconds"
    time.sleep(30)
    return JsonResponse({'success':200})

#客服登录
def user_login(request):
    username = request.POST['crmuser']
    password = request.POST['password']
    login_state = authenticate(username = username, password = password)
    if login_state['success']:
        request.session['user_id'] = login_state['content']
        user = UserInfo.objects.get(user_id = login_state['content'])
        userRoleList = UserRole.objects.filter(user_id = user.user_id)
        roleList = []
        for item in userRoleList:
            roleList.append(item.role_id)
        return JsonResponse({'success':0,'roleList':roleList})
    else:
        return JsonResponse({'success':1})

#认证
def authenticate(username = None, password = None):
    if UserInfo.objects.filter(user_name = username).exists():
        user = UserInfo.objects.get(user_name = username)
    else:
        return {'success':False}
    if user.user_password == password:
        return {'success':True,'content':user.user_id}
    else:
        return {'success':False}

def get_contact(request):
    contacts = Contact.objects.filter(contact_user_id = request.session['user_id'])
    contactsList = []
    status = request.GET['status']
    roleList = UserRole.objects.filter(user_id = request.session['user_id'])
    for role in roleList:
        contacts = Contact.objects.filter(contact_user_id = role.role_id)
        for item in contacts:
            if item.task_status == status:
                contactClient = ContactClient.objects.get(contact_id = item.contact_id)
                client = Client.objects.get(client_id =contactClient.client_id)
                content = {'contact_id':item.contact_id,'client_id':client.client_id,'contact_type':item.contact_type,'contact_date':item.contact_date,'contact_detail':item.contact_detail,'contact_type':item.contact_type,'customer_name':client.customer_name,'mobile':client.mobile,'customer_email':client.customer_email,'status':item.task_status,'contact_record':item.contact_record,'record_date':item.record_date,'note':item.note,'updated_by':item.updated_by}
                contactsList.append(content)
    if status == '1':
        contactsList.sort(key = operator.itemgetter('record_date'),reverse=True)
    if status == '2':
        contactsList.sort(key = operator.itemgetter('contact_date'),reverse=True)
    return JsonResponse({'contactsList':contactsList})

def get_users(request):
    users = UserInfo.objects.all()
    usersList = []
    for item in users:
        appendItem = True
        roleList = UserRole.objects.filter(user_id = item.user_id)
        for role in roleList:
            if role.role_id == 1004 or role.role_id == 1005:
                appendItem = False
        if appendItem:
            content = {'user_id':item.user_id,'user_name':item.user_name}
            usersList.append(content)
    return JsonResponse({'userList':usersList,'user_id':request.session['user_id']})

def get_message(request):
    status = request.GET['status']
    if status == '1':
        messages_all = Message.objects.filter(status = status).order_by('-revert_date')
    else:
        messages_all = Message.objects.filter(status = status).order_by('-message_time')
    messages_paginator = Paginator(messages_all,8)
    messages = messages_paginator.page(int(request.GET['page']))
    messageList = []

    for item in messages:
        content = {'messageID':item.message_id,'username':item.username,'mobile':item.mobile,'email':item.email,'message':item.message,'revert_record':item.revert_record,
                   'contact_date':item.contact_date,'contact_time':item.contact_time,'revert_record':item.revert_record,'status':item.status,
                   'updated_by':item.updated_by,'message_time':item.message_time,'revert_date':item.revert_date,'exist':'0','existList':""}
        clients = Client.objects.filter(customer_name = item.username)
        if clients.exists():
            content['exist'] = '1'
            clientList = []
            for item in clients:
                client_content = {'client_id':item.client_id}
                clientList.append(client_content)
            content['existList'] = clientList
        messageList.append(content)
    return JsonResponse({'messageList':messageList,'pageCount':messages_paginator.num_pages})

def save_revert_record(request):
    message = Message.objects.get(message_id=request.GET['message_id'])
    user = UserInfo.objects.get(user_id = request.session['user_id'])
    message.revert_record = request.GET['revert_record']
    message.revert_date = time.time()
    message.updated_by = user.user_name
    message.status = 1
    message.save()
    return JsonResponse({'success':200})

def new_contact(request):
    try:
        user = UserInfo.objects.get(user_id = request.session['user_id'])
        client_id = request.GET['client_id']
        user_id = request.GET['user_id']
        date = request.GET['date']
        time = request.GET['time']
        state = request.GET['state']
        details = request.GET['details']
        contact_date = date+' '+time
        contact = Contact(contact_date=contact_date,contact_user_id=user_id,contact_detail=details,contact_record='',task_status=state,contact_type=1,created_by=user.user_name,updated_by=user.user_name)
        contact.save()
        if contact.task_status == '1':
            contact.record_date = contact_date
            contact.save()
        contactClient = ContactClient(contact_id=contact.contact_id,client_id=client_id,created_by=user.user_name,updated_by=user.user_name)
        contactClient.save()
        logcat = open("logcat.txt", 'a')
        logcat.write('Time:'+str(get_time_details())+'  '+'User:'+str(user.user_name)+'\n')
        logcat.write('Action:Create a contact with ID '+str(contact.contact_id)+' about client '+str(contactClient.client_id)+'\n')
        logcat.write('Details:contact_date:'+str(contact.contact_date)+' contact_user_id:'+str(contact.contact_user_id)+' contact_detail:'+str(contact.contact_detail)+' contact_record:'+str(contact.contact_record)+' task_status:'+str(contact.task_status)+' contact_type:'+str(contact.contact_type)+' contact_user_id:'+str(contact.contact_user_id)+' created_by:'+str(contact.created_by)+' updated_by:'+str(contact.updated_by))
        logcat.write('\n')
        logcat.write('-------------------')
        logcat.write('\n')
        logcat.close()
        return JsonResponse({'success':0})
    except:
        return JsonResponse({'success':1})

def sendUserInfo(request):
    try:
        uesrInfo = request.GET['userInfo']
        indentity = request.GET['indentity']
        test = request.GET['test']
        asset = request.GET['asset']
        first = request.GET['first']

        print uesrInfo,indentity,test,asset
        return JsonResponse({'resultCode':200,'errorMsg':'No Error,Success!'})
    except:
        return JsonResponse({'resultCode':403,'errorMsg':'Parameter Error!'})

def getAuthority(request):
    try:
        user = UserInfo.objects.get(user_id = request.session['user_id'])
        userRoleList = UserRole.objects.filter(user_id = user.user_id)
        roleList = []
        for item in userRoleList:
            roleList.append(item.role_id)
        return JsonResponse({'roleList':roleList})
    except:
        return JsonResponse({})


def getManager(request):
    managers = Dictionary.objects.filter(type = '基金经理')
    managerList = []
    for item in managers:
        content = {'name':item.name,'value':item.value}
        managerList.append(content)
    return JsonResponse({'managerList':managerList})

def getuploadData(request):
    documentList = check_info(request.POST['tradeID'])
    return JsonResponse({'documentList':documentList})

def uploadData(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    tradeID = request.POST['tradeID']
    name = request.POST['name']
    type = request.POST['type']
    docContent = request.POST['imageContent']
    docBase64 = docContent.encode('utf-8')
    docList = docBase64.split('base64,')
    docData = base64.b64decode(docList[1])
    t = threading.Thread(target=saveInSQL, args=(tradeID,name,type,docData,userinfo,))
    t.start()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/tempfiles');
    newImg = open(REPORT_ROOT+'/'+name.encode('utf-8'),'wb')
    newImg.write(docContent)
    newImg.close()
    return JsonResponse({'url':name})

def saveInSQL(tradeID,docName,docType,docContent,userinfo):
    newDocument = Documentscan(document_name = docName,size=len(docContent),document_type = docType, content = docContent, upload_date=time.time(),created_by = userinfo.user_name, updated_by = userinfo.user_name)
    newDocument.save(using='fund_report')
    if TradeDocument.objects.filter(trade_id = tradeID).exists():
        tradeDocumentList = TradeDocument.objects.filter(trade_id = tradeID)
        for item in tradeDocumentList:
            document = Documentscan.objects.using('fund_report').get(id = item.document_id)
            if document.document_type == newDocument.document_type:
                TradeDocument.objects.get(trade_id = tradeID, document_id = document.id).delete()
    tradeDocument = TradeDocument(trade_id = tradeID, document_id = newDocument.id,created_by = userinfo.user_name, updated_by = userinfo.user_name)
    tradeDocument.save()

def check_info(tradeID):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_ROOT = os.path.join(BASE_DIR, 'gaoyicrm/static/tempfiles')
    tradeDocumentList = TradeDocument.objects.filter(trade_id = tradeID)
    documentList = []
    for item in tradeDocumentList:
        document = Documentscan.objects.using('fund_report').get(id = item.document_id)
        WriteFileData = open(REPORT_ROOT+'/'+str(document.id)+'_'+(document.document_name).encode('utf-8'),'wb')
        WriteFileData.write(document.content)
        WriteFileData.close()
        documentList.append({'name':str(document.id)+'_'+(document.document_name).encode('utf-8'),'type':document.document_type})
    return documentList

def getTradeDoc(request):
    tradeID = request.GET['tradeID']
    print tradeID
    tradeScan = TradeScan.objects.get(trade_id = tradeID)
    print tradeScan
    return JsonResponse({'location':tradeScan.object_info})


def saveTradeDoc(request):
    userinfo = UserInfo.objects.get(user_id = request.session["user_id"])
    tradeID = request.GET['tradeID']
    location = request.GET['location']
    if TradeScan.objects.filter(trade_id = tradeID).exists():
        tradeScan = TradeScan.objects.get(trade_id = tradeID)
        tradeScan.object_info = location
        tradeScan.object_operator = userinfo.user_name
        tradeScan.save()
    else:
        tradeScan = TradeScan(trade_id = tradeID, object_info = location, object_operator = userinfo.user_name, created_by = userinfo.user_name, updated_by = userinfo.user_name)
        tradeScan.save()
    return JsonResponse({})
