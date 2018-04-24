"""GaoYi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from gaoyicrm.upload import upload_image
from gaoyicrm.views import account_editor,account_org_editor,account_task,bind_weixin,bespeak,getAuthority,changeVersions,changeToChinese,changeToEnglish,loginOrNot,logout,home,login,commitment,register,retrieve,authentication,leave_message,manageMedia, \
    check_name,send_code,check_code,check_mobile,store_info,check_identity_card,fund_details,fund_info, \
    update_identity_card,check_phone_exist,check_identity_typed,check_matched,update_password,change_password,\
    account_home,account_details,accout_inquiry,check_status,account_personal,account_product, \
    get_home,account_home_info,fund_details_chart,get_inquiry,get_product,getRecommendedFunds,get_ready_for_bespeak,account_bespeak,store_inquery,delete_inquery, \
    company,trends_media,get_articles,trends_research,trends_media_info,trends_research_info,get_records,chooseUser,loginPart, \
    investTeam_qgl,investTeam_news_qgl,investTeam_news_qgl_info,investTeam_dxf,investTeam_news_dxf,investTeam_news_dxf_info,investTeam_sqr,investTeam_news_sqr,investTeam_news_sqr_info, \
    investTeam_zlw,investTeam_news_zlw,investTeam_news_zlw_info,investTeam_fl,investTeam_news_fl,investTeam_news_fl_info,investTeam_wsh,investTeam_news_wsh,investTeam_news_wsh_info,contact_information,contact_recruitment,contact_recruitment_info,questionnaire,org_questionnaire,riskEvaluation_result,org_riskEvaluation_result
from gaoyicrm.utils import account_modifyPassword,checkPassword,account_modifyEmail,modifyAddress,modifyPhone1,modifyPhone2,account_modifyAddress,account_modifyPhone,account_modifyOccupation,modifyOccupation,emailAuthentication,get_bespeak,result,report,sendmail,weixininfo,finishOrNot,bangding

from gaoyicrm.crm import sleepRequest,get_contact,user_login,new_contact,get_message,save_revert_record,get_users,sendUserInfo,getAuthority,getManager,uploadData,getuploadData,saveTradeDoc,getTradeDoc
from gaoyicrm.crm_user import edit_email_client,account_upload,save_contact_record,checkBaseInfo,changeRiskType,getAvailableShares,exportMsg,getTotalApplyList,account_function,account_records,search_user,get_user_count,get_client_list,get_user_details,edit_crm_client,edit_client,infoAboutAuestionnaire,ResultAboutAuestionnaire,ResultAboutQuestionnaire,\
    get_user_edit,delet_client,check_client,get_user_fund_time,get_client_classify,task_detail,message_detail,get_task_detail,get_detail_message,search_classify_user,get_estimate_nav,account_intention,account_check,getApplyList,getFundsList,getFuzzyProduct,saveApply,deleteApply,imageUpload,deleteInAccredited,account_apply,account_add_apply,account_redemption_apply,judgeAcc,applyDetails,updateClientAccount,xlsHandle,getClientCheck,getClientDoc,sentInfoMail,riskEnsure
from django.conf import settings
from gaoyicrm.test import getmytest

urlpatterns = [
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r"^uploads/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT,}),
    url(r'^gymgmt/', include(admin.site.urls)),


    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r'^changeVersions/', changeVersions, name='changeVersions'),
    url(r'^changeToChinese/', changeToChinese, name='changeToChinese'),
    url(r'^changeToEnglish/', changeToEnglish, name='changeToEnglish'),

    url(r'^loginOrNot/', loginOrNot, name='loginOrNot'),
    url(r'^logout/', logout, name='logout'),

    url(r'^$', login, name='home'),
    # url(r'promise/', promise, name='promise'),
    # url(r'^promiseOrNot/', promiseOrNot, name='promiseOrNot'),
    # url(r'givePromise/', givePromise, name='givePromise'),

    # url(r'^login/', login, name='login'),
    url(r'^commitment/', commitment, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^retrieve/', retrieve, name='retrieve'),
    url(r'^authentication/(.+)', authentication, name='authentication'),

    url(r'^manageMedia/', manageMedia, name='manageMedia'),

    url(r'^fund_details_chart/', fund_details_chart, name='fund_details_chart'),

    url(r'^company/', company, name='company'),
    url(r'^fund_details/', fund_details, name='fund_details'),
    url(r'^fund_info/', fund_info, name='fund_info'),

    url(r'^contact_information/', contact_information, name='contact_information'),
    url(r'^contact_recruitment/', contact_recruitment, name='contact_recruitment'),
    url(r'^contact_recruitment_info/(.+)', contact_recruitment_info, name='contact_recruitment_info'),

    url(r'^bespeak/', bespeak, name='bespeak'),
    url(r'^weixininfo/', weixininfo, name='weixininfo'),

    url(r'^trends_media/', trends_media, name='trends_media'),
    url(r'^get_articles/', get_articles, name='get_articles'),
    url(r'^trends_research/', trends_research, name='trends_research'),
    url(r'^trends_media_info/(.+)', trends_media_info, name='trends_media_info'),
    url(r'^trends_research_info/(.+)', trends_research_info, name='trends_research_info'),

    url(r'^investTeam_qgl/', investTeam_qgl, name='investTeam_qgl'),
    url(r'^investTeam_dxf/', investTeam_dxf, name='investTeam_dxf'),
    url(r'^investTeam_sqr/', investTeam_sqr, name='investTeam_sqr'),
    url(r'^investTeam_zlw/', investTeam_zlw, name='investTeam_zlw'),
    url(r'^investTeam_fl/', investTeam_fl, name='investTeam_fl'),
    url(r'^investTeam_wsh/', investTeam_wsh, name='investTeam_wsh'),
    url(r'^investTeam_news_qgl/', investTeam_news_qgl, name='investTeam_news_qgl'),
    url(r'^investTeam_news_qgl_info/(.+)', investTeam_news_qgl_info, name='investTeam_news_qgl_info'),
    url(r'^investTeam_news_dxf/', investTeam_news_dxf, name='investTeam_news_dxf'),
    url(r'^investTeam_news_dxf_info/(.+)', investTeam_news_dxf_info, name='investTeam_news_dxf_info'),
    url(r'^investTeam_news_sqr/', investTeam_news_sqr, name='investTeam_news_sqr'),
    url(r'^investTeam_news_sqr_info/(.+)', investTeam_news_sqr_info, name='investTeam_news_sqr_info'),
    url(r'^investTeam_news_zlw/', investTeam_news_zlw, name='investTeam_news_zlw'),
    url(r'^investTeam_news_zlw_info/(.+)', investTeam_news_zlw_info, name='investTeam_news_zlw_info'),
    url(r'^investTeam_news_fl/', investTeam_news_fl, name='investTeam_news_fl'),
    url(r'^investTeam_news_fl_info/(.+)', investTeam_news_fl_info, name='investTeam_news_fl_info'),
    url(r'^investTeam_news_wsh/', investTeam_news_wsh, name='investTeam_news_wsh'),
    url(r'^investTeam_news_wsh_info/(.+)', investTeam_news_wsh_info, name='investTeam_news_wsh_info'),

    url(r'^account_home_info/', account_home_info, name='account_home_info'),
    url(r'^account_home/', account_home, name='account_home'),
    url(r'^account_details/', account_details, name='account_details'),
    url(r'^account_product/', account_product, name='account_product'),
    url(r'^account_records/', account_records, name='account_records'),
    url(r'^account_inquiry/', accout_inquiry, name='accout_inquiry'),
    url(r'^account_personal/', account_personal, name='account_personal'),
    url(r'^account_bespeak/', account_bespeak, name='account_bespeak'),
    url(r'^get_bespeak/', get_bespeak, name='get_bespeak'),

    url(r'^store_inquery/', store_inquery, name='store_inquery'),
    url(r'^delete_inquery/', delete_inquery, name='delete_inquery'),

    url(r'^get_ready_for_bespeak/', get_ready_for_bespeak, name='get_ready_for_bespeak'),

    url(r'^get_home/', get_home, name='get_home'),
    url(r'^getRecommendedFunds/', getRecommendedFunds, name='getRecommendedFunds'),
    url(r'^get_records/', get_records, name='get_records'),
    url(r'^get_inquiry/', get_inquiry, name='get_inquiry'),
    url(r'^get_product/', get_product, name='get_product'),

    url(r'^check_name', check_name, name='check_name'),
    url(r'^check_mobile', check_mobile, name='check_mobile'),
    url(r'^send_code', send_code, name='send_code'),
    url(r'^check_code', check_code, name='check_code'),
    url(r'^store_info', store_info, name='store_info'),

    url(r'^check_status',check_status,name='check_status'),

    url(r'^leave_message',leave_message,name='leave_message'),

    url(r'^check_identity_card', check_identity_card, name='check_identity_card'),
    url(r'^update_identity_card', update_identity_card, name='update_identity_card'),

    url(r'^questionnaire', questionnaire, name='questionnaire'),
    url(r'^org_questionnaire', org_questionnaire, name='org_questionnaire'),
    url(r'^infoAboutAuestionnaire', infoAboutAuestionnaire, name='infoAboutAuestionnaire'),
    url(r'^ResultAboutAuestionnaire', ResultAboutAuestionnaire, name='ResultAboutAuestionnaire'),
    url(r'^ResultAboutQuestionnaire', ResultAboutQuestionnaire, name='ResultAboutQuestionnaire'),
    url(r'^riskEvaluation_result', riskEvaluation_result, name='riskEvaluation_result'),
    url(r'^org_riskEvaluation_result', org_riskEvaluation_result, name='org_riskEvaluation_result'),

    url(r'^result', result, name='result'),

    url(r'^getAuthority', getAuthority, name='getAuthority'),
    url(r'^report', report, name='report'),
    url(r'^sendmail', sendmail, name='sendmail'),

    url(r'^account_apply',account_apply,name='account_apply'),
    url(r'^account_add_apply',account_add_apply,name='account_add_apply'),
    url(r'^account_redemption_apply',account_redemption_apply,name='account_redemption_apply'),
    url(r'^modifyAddress', modifyAddress, name='modifyAddress'),
    url(r'^modifyPhone1', modifyPhone1, name='modifyPhone1'),
    url(r'^modifyPhone2', modifyPhone2, name='modifyPhone2'),
    url(r'^account_modifyAddress', account_modifyAddress, name='account_modifyAddress'),
    url(r'^account_editor', account_editor, name='account_editor'),
    url(r'^account_org_editor',account_org_editor,name='account_org_editor'),
    url(r'^account_task', account_task, name='account_task'),
    url(r'^account_modifyPhone', account_modifyPhone, name='account_modifyPhone'),
    url(r'^account_modifyEmail', account_modifyEmail, name='account_modifyEmail'),
    url(r'^account_modifyOccupation', account_modifyOccupation, name='account_modifyOccupation'),
    url(r'^account_modifyPassword',account_modifyPassword,name='account_modifyPassword'),
    url(r'^checkPassword',checkPassword,name='checkPassword'),

    url(r'^check_phone_exist', check_phone_exist, name='check_phone_exist'),
    url(r'^check_identity_typed', check_identity_typed, name='check_identity_typed'),
    url(r'^check_matched', check_matched, name='check_matched'),
    url(r'^update_password',update_password,name='update_password'),
    url(r'^change_password',change_password,name='change_password'),

    url(r'^emailAuthentication',emailAuthentication,name='emailAuthentication'),
    url(r'^modifyOccupation',modifyOccupation,name='modifyOccupation'),

    url(r'^bangding',bangding,name='bangding'),
    url(r'^chooseUser',chooseUser,name='chooseUser'),
    url(r'^loginPart',loginPart,name='loginPart'),
    url(r'^bind_weixin',bind_weixin,name='bind_weixin'),
    url(r'^finishOrNot',finishOrNot,name='finishOrNot'),


    url(r'^user_login',user_login,name='user_login'),

    url(r'^search_user',search_user,name='search_user'),
    url(r'^get_user_count',get_user_count,name='get_user_count'),

    url(r'^get_user_details',get_user_details,name='get_user_details'),

    url(r'^new_contact',new_contact,name='new_contact'),
    url(r'^get_contact',get_contact,name='get_contact'),
    url(r'^edit_crm_client',edit_crm_client,name='edit_crm_client'),
    url(r'^edit_client',edit_client,name='edit_client'),
    url(r'^get_users',get_users,name='get_users'),
    url(r'^get_user_edit',get_user_edit,name='get_user_edit'),
    url(r'^get_user_fund_time',get_user_fund_time,name='get_user_fund_time'),
    url(r'^get_client_list',get_client_list,name='get_client_list'),
    url(r'^get_client_classify',get_client_classify,name='get_client_classify'),
    url(r'^get_message',get_message,name='get_message'),
    url(r'^save_revert_record',save_revert_record,name='save_revert_record'),
    url(r'^save_contact_record',save_contact_record,name='save_contact_record'),

    url(r'^account_function',account_function,name='account_function'),
    url(r'^task_detail',task_detail,name='task_detail'),
    url(r'^message_detail',message_detail,name='message_detail'),
    url(r'^get_task_detail',get_task_detail,name='get_task_detail'),
    url(r'^get_detail_message',get_detail_message,name='get_detail_message'),

    url(r'^search_classify_user',search_classify_user,name='search_classify_user'),
    url(r'^delet_client',delet_client,name='delet_client'),
    url(r'^check_client',check_client,name='check_client'),
    url(r'^getmytest',getmytest,name='getmytest'),

    url(r'^get_estimate_nav',get_estimate_nav,name='get_estimate_nav'),
    url(r'^account_intention',account_intention,name='account_intention'),
    url(r'^account_check',account_check,name='account_check'),

    url(r'^getApplyList',getApplyList,name='getApplyList'),
    url(r'^getFundsList',getFundsList,name='getFundsList'),
    url(r'^getFuzzyProduct',getFuzzyProduct,name='getFuzzyProduct'),

    url(r'^deleteApply',deleteApply,name='deleteApply'),
    url(r'^saveApply',saveApply,name='saveApply'),

    url(r'^sendUserInfo',sendUserInfo,name='sendUserInfo'),

    url(r'^applyDetails',applyDetails,name='applyDetails'),
    url(r'^judgeAcc',judgeAcc,name='judgeAcc'),
    url(r'^imageUpload',imageUpload,name='imageUpload'),
    url(r'^deleteInAccredited',deleteInAccredited,name='deleteInAccredited'),
    url(r'^updateClientAccount',updateClientAccount,name='updateClientAccount'),
    url(r'^xlsHandle',xlsHandle,name='xlsHandle'),
    url(r'^getClientCheck',getClientCheck,name='getClientCheck'),
    url(r'^getClientDoc',getClientDoc,name='getClientDoc'),

    url(r'^sentInfoMail',sentInfoMail,name='sentInfoMail'),

    url(r'^getAvailableShares',getAvailableShares,name='getAvailableShares'),
    url(r'^changeRiskType',changeRiskType,name='changeRiskType'),

    url(r'^getTotalApplyList',getTotalApplyList,name='getTotalApplyList'),
    url(r'^exportMsg',exportMsg,name='exportMsg'),

    url(r'^getAuthority',getAuthority,name='getAuthority'),

    url(r'^checkBaseInfo',checkBaseInfo,name='checkBaseInfo'),

    url(r'^get_manager',getManager,name='getManager'),

    url(r'^account_upload',account_upload,name='account_upload'),

    url(r'^uploadData',uploadData,name='uploadData'),

    url(r'^getuploadData',getuploadData,name='getuploadData'),

    url(r'^saveTradeDoc',saveTradeDoc,name='saveTradeDoc'),

    url(r'^getTradeDoc',getTradeDoc,name='getTradeDoc'),

    url(r'^riskEnsure',riskEnsure,name='riskEnsure'),
   
    url(r'^edit_email_client',edit_email_client,name='edit_email_client'),
    url(r'^sleepRequest',sleepRequest),
]
