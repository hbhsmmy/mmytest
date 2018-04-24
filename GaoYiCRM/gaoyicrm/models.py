# -*- coding: utf-8 -*-
from django.db import models
import django.utils.timezone as timezone
import hashlib

# 用户模型.
class Investor(models.Model):
    username = models.CharField(max_length=40, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    realname = models.CharField(max_length=16, verbose_name='真实姓名')
    idtype = models.IntegerField(verbose_name='证件类型')
    idno = models.CharField(max_length=32, verbose_name='证件号码')
    email = models.CharField(max_length=128, verbose_name='电子邮箱')
    openid = models.CharField(max_length=128, verbose_name='OPEN ID')
    taid = models.CharField(max_length=128, verbose_name='TA ID')
    education = models.CharField(max_length=128, verbose_name='学历')
    occupation = models.CharField(max_length=128, verbose_name='职业')
    point = models.CharField(max_length=128, verbose_name='分数')
    address = models.CharField(max_length=256, verbose_name='地址',default='_')
    appendage = models.CharField(max_length=512, verbose_name='备用附加')
    registertime = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        verbose_name = '用户'
        db_table = "investor"

    def __unicode__(self):
        return self.username
#
# 预约模型.
class Inquiry(models.Model):
    userid = models.CharField(max_length=40, verbose_name='用户ID')
    realname = models.CharField(max_length=16, verbose_name='真实姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    email = models.CharField(max_length=128, verbose_name='电子邮箱')
    message = models.CharField(max_length=999,verbose_name='留言')
    inquirytype = models.CharField(max_length=10,verbose_name='预约类型')
    fundname = models.CharField(max_length=32, verbose_name='基金名字')
    date = models.CharField(max_length=20, verbose_name='日期')
    time = models.CharField(max_length=20, verbose_name='时间')
    inquirytime = models.DateTimeField(auto_now_add=True, verbose_name='预约时间')
    inquirystate = models.IntegerField(verbose_name='预约状态')

    class Meta:
        verbose_name = '预约'
        db_table = "inquiry"

    def __unicode__(self):
        return self.fundname

# 招聘模型.
class Job(models.Model):
    title = models.CharField(max_length=40, verbose_name='标题')
    address = models.CharField(max_length=40, verbose_name='工作地点')
    number = models.CharField(max_length=10, verbose_name='需求人数')
    duty = models.CharField(max_length=999, verbose_name='工作职责')
    demand = models.CharField(max_length=999,verbose_name='任职条件')

    class Meta:
        verbose_name = '招聘'
        db_table = "job"

    def __unicode__(self):
        return self.title

# class Message(models.Model):
#     username = models.CharField(max_length=16, verbose_name='真实姓名')
#     mobile = models.CharField(max_length=11, verbose_name='手机号码')
#     email = models.CharField(max_length=128, verbose_name='电子邮箱')
#     message = models.CharField(max_length=999, verbose_name='用户留言')
#     date = models.CharField(max_length=20, verbose_name='日期')
#     time = models.CharField(max_length=20, verbose_name='时间')
#
#     class Meta:
#         verbose_name = '留言'
#         db_table = "message"
#
#     def __unicode__(self):
#         return self.username

class Message(models.Model):
    message_id      =  models.AutoField(primary_key=True,auto_created=True,verbose_name='留言id')
    message_time    = models.DateTimeField(verbose_name='留言时间')
    source  = models.CharField(max_length=10, blank=True, null=True,    verbose_name='来源1网站2微信')
    username = models.CharField(max_length=100, blank=True, null=True,    verbose_name='留言客户名')
    mobile = models.CharField(max_length=50, blank=True, null=True,    verbose_name='手机号码')
    email  = models.CharField(max_length=128, blank=True, null=True,   verbose_name='邮箱')
    message = models.CharField(max_length=999, blank=True, null=True,   verbose_name='留言内容')
    contact_date  = models.CharField(max_length=32, blank=True, null=True,   verbose_name='期望接触日期')
    contact_time  = models.CharField(max_length=32, blank=True, null=True,   verbose_name='期望接触时间')
    revert_record = models.CharField(max_length=500, blank=True, null=True,verbose_name='回复记录')
    revert_date   = models.CharField(max_length=50, blank=True, null=True,verbose_name='回复时间')
    status = models.CharField(max_length=8, blank=True, null=True,verbose_name='状态')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '网站留言表'
        ordering = ['-message_id']
        db_table = "message_tbl"

    def __unicode__(self):
        return self.username


# 自定义一个文章Model的管理器
# 1、新加一个数据处理的方法
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

# 文章模型
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    brief_comment = models.TextField(max_length=150, verbose_name='文章简评')
    author = models.CharField(max_length=50, verbose_name='文章作者')
    content = models.TextField(max_length=100000,verbose_name='文章内容')
    ARTICLE_TYPE = (
        (0, '不属于任何'),
        (1, '高毅精选'),
        (2, '财富观察'),
    )
    type = models.IntegerField(default=0, choices=ARTICLE_TYPE, verbose_name='文章类型')
    MANAGER_TYPE = (
        (0, '不属于任何'),
        (1, '邱国鹭'),
        (2, '邓晓峰'),
        (3, '孙庆瑞'),
        (4, '卓利伟'),
        (5, '冯柳'),
        (6, '王世宏')
    )
    manager = models.IntegerField(default=0, choices=MANAGER_TYPE, verbose_name='所属基金经理')
    is_homepage = models.BooleanField(default=False, verbose_name='是否首页')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateField(default=timezone.now, editable=True, verbose_name='发布时间')
    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title

class Customer(models.Model):
    customerName = models.CharField(max_length=50, verbose_name='姓名')
    positionPost = models.CharField(max_length=50, verbose_name='职位')
    address = models.CharField(max_length=50, verbose_name='地点')
    mobile = models.CharField(max_length=50, verbose_name='电话')
    email = models.CharField(max_length=50, verbose_name='邮件')
    status = models.IntegerField(default=0, verbose_name='工作状态')

    class Meta:
        verbose_name = '客服'

    def __unicode__(self):
        return self.customerName

class recommendedFund(models.Model):
    fundId = models.CharField(max_length=50, verbose_name='基金ID')
    fundName = models.CharField(max_length=50, verbose_name='基金名称')
    isRecommended = models.BooleanField(default=False, verbose_name='是否推荐')

    class Meta:
        verbose_name = '基金推荐表'

    def __unicode__(self):
        return self.fundName

# 用户表
class UserInfo(models.Model):
    user_id      = models.AutoField(primary_key=True,auto_created=True,verbose_name='用户id')
    user_password= models.CharField(max_length=100, verbose_name='用户密码')
    user_name	   = models.CharField(max_length=100, verbose_name='用户姓名')
    user_dept	   = models.CharField(max_length=32, blank=True, null=True,   verbose_name='用户部门')
    user_mobile 	= models.CharField(max_length=32, verbose_name='用户手机电话')
    user_office_phone	= models.CharField(max_length=32, verbose_name='用户办公座机')
    user_email	      = models.CharField(max_length=50, verbose_name='用户公司邮箱')
    user_email_personal	= models.CharField(max_length=50, blank=True, null=True,   verbose_name='用户个人邮箱')
    user_office_city	= models.CharField(max_length=50, blank=True, null=True,   verbose_name='用户办公base地点')
    user_wx	= models.CharField(max_length=20, blank=True, null=True,   verbose_name='用户微信号')
    user_open_id	= models.CharField(max_length=32, blank=True, null=True,  verbose_name='用户微信open_id')
    address	= models.CharField(max_length=256, blank=True, null=True,  verbose_name='地址')
    note	  = models.CharField(max_length=100, blank=True, null=True,  verbose_name='备注')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户表'
        db_table = "user_info_tbl"

    def __unicode__(self):
        return  self.user_name

class Client(models.Model):
    client_id = models.AutoField(primary_key=True, auto_created=True, verbose_name='客户id')
    password = models.CharField(max_length=32, verbose_name='密码')
    ta_id = models.CharField(max_length=40, unique=True, blank=True, null=True, verbose_name='TAID')
    mark = models.CharField(max_length=10, blank=False, verbose_name='是否同步客户：1正式 2潜客 3网站但无TAID客户')
    source_type = models.CharField(max_length=10, blank=True, null=True, verbose_name='渠道类型1直销2代销3无')
    customer_name = models.CharField(max_length=64, blank=False, verbose_name='客户姓名')
    customer_type = models.CharField(max_length=10, blank=False, verbose_name='客户类型')
    id_type = models.CharField(max_length=8, blank=True, null=True, verbose_name='证件类型')
    id_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='证件号码')
    sex = models.CharField(max_length=8, blank=True, null=True, verbose_name='性别')
    birthday = models.CharField(max_length=32, blank=True, null=True, verbose_name='生日')
    customer_manager = models.CharField(max_length=32, blank=True, null=True, verbose_name='客户经理')
    client_source_desc = models.CharField(max_length=32, blank=True, null=True, verbose_name='客户来源')
    prime_id = models.CharField(max_length=40, blank=True, null=True, verbose_name='合并到主客户ID')
    mobile = models.CharField(max_length=30, blank=True, null=True, verbose_name='客户电话')
    customer_email = models.CharField(max_length=50, blank=True, null=True, verbose_name='客户电子邮件')
    customer_wx = models.CharField(max_length=50, blank=True, null=True, verbose_name='微信')
    open_id = models.CharField(max_length=128, blank=True, null=True, verbose_name='微信openId', default='_')
    investor_id = models.IntegerField(blank=True, null=True, verbose_name='网站用户id')
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name='网站用户名', default='_')
    contact_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='联系人')
    contact_mobile = models.CharField(max_length=30, blank=True, null=True, verbose_name='联系人电话', default='_')
    interest = models.CharField(max_length=500, blank=True, null=True, verbose_name='感兴趣内容')
    province = models.CharField(max_length=20, blank=True, null=True, verbose_name='省份')
    city = models.CharField(max_length=20, blank=True, null=True, verbose_name='所在城市')
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name='联系地址')
    nationality = models.CharField(max_length=64, blank=True, null=True, verbose_name='国籍')
    education = models.CharField(max_length=128, blank=True, null=True, verbose_name='学历')
    zipcode = models.CharField(max_length=8, blank=True, null=True, verbose_name='邮政编码')
    occupation = models.CharField(max_length=128, blank=True, null=True, verbose_name='职业')
    position = models.CharField(max_length=128, blank=True, null=True, verbose_name='职务')
    employer = models.CharField(max_length=128, blank=True, null=True, verbose_name='工作单位')
    valid_begin = models.CharField(max_length=32, blank=True, null=True, verbose_name='证件起始期')
    valid_end = models.CharField(max_length=32, blank=True, null=True, verbose_name='证件失效期')
    represent1 = models.CharField(max_length=256, blank=True, null=True, verbose_name='法定代表人')
    represent_idtype = models.CharField(max_length=256, blank=True, null=True, verbose_name='代表人证件类型')
    represent_idno = models.CharField(max_length=256, blank=True, null=True, verbose_name='代表人证件号码')
    controller = models.CharField(max_length=128, blank=True, null=True, verbose_name='机构实际控股人')
    businessscope = models.CharField(max_length=256, blank=True, null=True, verbose_name='机构经营范围')
    risk_type = models.CharField(max_length=32, blank=True, null=True, verbose_name='客户最新的风险问卷测评分数')
    status = models.CharField(max_length=8, blank=False, verbose_name='状态1有效2失效')
    created_by = models.CharField(max_length=50, blank=False, verbose_name='创建人')
    created_date = models.DateTimeField(auto_now_add=True, blank=False, verbose_name='创建时间')
    updated_by = models.CharField(max_length=50, blank=False, verbose_name='上次修改人')
    updated_date = models.DateTimeField(auto_now_add=True, blank=False, verbose_name='修改时间')

    class Meta:
        verbose_name = 'CRM客户基本信息表'
        db_table = "client_tbl"

    def __unicode__(self):
        return self.customer_name

# 客户感兴趣的基金经理表
class InterestManager(models.Model):
    interest_relate_id = models.AutoField(primary_key=True,auto_created=True,verbose_name='表主键id')
    client       = models.ForeignKey(Client)
    manager_id    = models.CharField(max_length=40, verbose_name='基金经理id')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '客户感兴趣的基金经理表'
        db_table = "interest_manager_tbl"

    def __unicode__(self):
        return self.manager_id


# 字典表
class Dictionary(models.Model):
    id =  models.AutoField(primary_key=True,auto_created=True,verbose_name='字典表主键')
    type = models.CharField(max_length=40, verbose_name='常量类型')
    value = models.CharField(max_length=10, verbose_name='值')
    name = models.CharField(max_length=50,verbose_name='名称')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '字典表'
        db_table = "dictionary_tbl"

    def __unicode__(self):
        return '%s %s' % (self.value, self.name)

# 待办和接触历史表
class Contact(models.Model):
    contact_id     = models.AutoField(primary_key=True,auto_created=True,verbose_name='接触历史的id')
    contact_date   = models.CharField(max_length=50, blank=True, null=True,verbose_name='接触时间/待办计划完成时间')
    contact_user   = models.ForeignKey(UserInfo)
    contact_detail = models.CharField(max_length=500, blank=True, null=True,verbose_name='详细内容')
    contact_record = models.CharField(max_length=500, blank=True, null=True,verbose_name='处理情况记录')
    record_date    =  models.CharField(max_length=50, blank=True, null=True,verbose_name='处理时间')
    task_status = models.CharField(max_length=8, verbose_name='状态1已处理2未处理')
    contact_type  = models.CharField(max_length=50, blank=True, null=True, verbose_name='接触类型可空')
    contact_message_id  = models.CharField(max_length=40, blank=True, null=True, verbose_name='接触邮件或短信内容id可空')
    note =    models.CharField(max_length=256, blank=True, null=True, verbose_name='备注')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '接触历史表'
        db_table = "contact_tbl"

    def __unicode__(self):
        return  self.contact_detail


# 客户与接触关联关系表
class ContactClient(models.Model):
    contact = models.ForeignKey(Contact)
    client  = models.ForeignKey(Client)
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '客户与接触关联关系表'
        db_table = "contact_client_tbl"

    def __unicode__(self):
        return  self.created_by

# 岗位表
class RoleInfo(models.Model):
    role_id      =  models.AutoField(primary_key=True,auto_created=True,verbose_name='岗位id')
    role_name	  = models.CharField(max_length=100, verbose_name='岗位名称')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '岗位表'
        db_table = "role_info_tbl"

    def __unicode__(self):
        return  self.role_name


# 用户岗位关系表
class UserRole(models.Model):
    user = models.ForeignKey(UserInfo)
    role = models.ForeignKey(RoleInfo)
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '用户岗位关系表'
        db_table = "user_role_tbl"

    def __unicode__(self):
        return self.created_by

# 预约表
class Apply(models.Model):
    apply_id  =  models.AutoField(primary_key=True,auto_created=True,verbose_name='预约id')
    client    = models.ForeignKey(Client)
    fund_id	  = models.CharField(max_length=50, verbose_name='基金id')
    apply_date   = models.DateField(auto_now_add=True, verbose_name='预约开放日')
    apply_type   = models.CharField(max_length=8, verbose_name='预约类型1-认购2-追购3-赎回')
    apply_amount = models.FloatField(max_length=18, verbose_name='预约金额')
    apply_count  = models.FloatField(max_length=18, verbose_name='预约份额')
    apply_channel    = models.CharField(max_length=8, verbose_name='预约渠道1-线下2-网站')
    p_trade_id   = models.CharField(max_length=50, verbose_name='预约与交易对应关系对应的customer_trade表的tradeId')
    input_date    = models.CharField(max_length=32, verbose_name='录入时间')
    account_date  = models.CharField(max_length=32, verbose_name='到账时间')
    silence_date  = models.CharField(max_length=32, verbose_name='到期时间')
    HF_date       = models.CharField(max_length=32, verbose_name='回访时间')
    complete_date = models.CharField(max_length=32, verbose_name='完成时间')
    cancel_date   = models.CharField(max_length=32, verbose_name='失效时间')
    info_flag   = models.CharField(max_length=2, verbose_name='客户基本信息表是否签署并收回')
    idtype_flag = models.CharField(max_length=2, verbose_name='身份证件材料是否签署并收回')
    risk_flag   = models.CharField(max_length=2, verbose_name='风险提示文件是否签署并收回')
    questionnaire_flag = models.CharField(max_length=2, verbose_name='风险评估问卷是否填写并收回')
    asset_flag  = models.CharField(max_length=2, verbose_name='资产证明材料是否签署并收回')
    contract_flag = models.CharField(max_length=2, verbose_name='合同是否签署并收回')
    applytab_flag = models.CharField(max_length=2, verbose_name='直销申请表是否签署并收回')
    sign_contract_date  = models.CharField(max_length=32, verbose_name='合同签署日期')
    status    =  models.CharField(max_length=8, verbose_name='预约状态1-已录入2-已到账3-已回访4-已完成5-已失效')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '预约表'
        db_table = "apply_tbl"

    def __unicode__(self):
        return self.created_by

class Accredited(models.Model):
    accredited_id  =  models.AutoField(primary_key=True,auto_created=True,verbose_name='审核id')
    client    =  models.ForeignKey(Client)
    apply     =  models.ForeignKey(Apply)
    status    =  models.CharField(max_length=8, verbose_name='审核状态1-已录入未完整2-已录入已完整合格投资者3-已失效过期')
    failed_type =  models.CharField(max_length=8, verbose_name='失效/缺少的内容1-证件照片2-问卷3-资产证明')
    check_user  =  models.CharField(max_length=50, verbose_name='审核通过操作用户名，即上传材料的用户，若是系统自动复制创建则填入system')
    check_date  =  models.CharField(max_length=32, verbose_name='审核通过时间')
    created_by    =  models.CharField(max_length=50, verbose_name='创建人')
    created_date  =  models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    =  models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  =  models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '审核表'
        db_table = "accredited_tbl"

    def __unicode__(self):
        return self.created_by

class Document(models.Model):
    document_id   = models.AutoField(primary_key=True,auto_created=True,verbose_name='文件id')
    document_name = models.CharField(max_length=256, verbose_name='文件文档的名称含类型后缀')
    document_type = models.CharField(max_length=8, verbose_name='文件类型1-网站上传证件照片2-网站上填写并生成的问卷3-网站上传资产证明;4-网站上传机构授权书;5-收回签字后证件;6-收回签字后资产证明;7签字后问卷;8签字后合同(含风险揭示书)9-签字后直销申请表10签字后的客户信息表11其他')
    content = models.BinaryField(verbose_name='文档内容')
    size    = models.IntegerField(verbose_name='文档大小')
    upload_date = models.CharField(max_length=32, verbose_name='上传时间')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '审核及文件关联表'
        db_table = "document_tbl"

    def __unicode__(self):
        return self.document_tbl

class AccreditedDoc(models.Model):
    accredited =  models.ForeignKey(Accredited)
    document =  models.ForeignKey(Document)
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '审核及文件关联表'
        db_table = "accredited_doc_tbl"

    def __unicode__(self):
        return self.created_by

class ClientAccount(models.Model):
    client =  models.ForeignKey(Client)
    apply  =  models.ForeignKey(Apply)
    expire_date = models.CharField(max_length=32, verbose_name='失效日期')
    bank_name = models.CharField(max_length=128, verbose_name='客户开户行')
    account_name = models.CharField(max_length=128, verbose_name='客户账户名')
    account_no   = models.CharField(max_length=64, verbose_name='客户账号')
    note   = models.CharField(max_length=128, verbose_name='备注可以填入变更原因')
    status = models.CharField(max_length=8, verbose_name='状态1有效2失效')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '客户预约对应的银行信息'
        db_table = "client_account_tbl"

    def __unicode__(self):
        return self.bank_name


class Capital(models.Model):
    capital_id = models.AutoField(primary_key=True,auto_created=True,verbose_name='流水id')
    excel_input_id = models.CharField(max_length=64, verbose_name='excel中的记账流水号')
    fund_id = models.CharField(max_length=64, verbose_name='基金id')
    acc_account_no = models.CharField(max_length=64, verbose_name='我方产品收款账户')
    capital_date = models.CharField(max_length=32, verbose_name='我方产品收款时间')
    payee_account_name = models.CharField(max_length=64, verbose_name='客户付款账户名')
    payee_account_no = models.CharField(max_length=64, verbose_name='客户付款账号')
    credit_sum = models.FloatField(max_length=16, verbose_name='贷方金额，使用该金额匹配')
    vir_account_no = models.CharField(max_length=64, verbose_name='招证-虚拟编号')
    vir_account_name = models.CharField(max_length=64, verbose_name='招证-虚拟户户名')
    note = models.CharField(max_length=128, verbose_name='备注')
    status = models.CharField(max_length=128, verbose_name='状态1-已录入2-已匹配使用3-失效(3状态用于以后备用)')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '流水表'
        db_table = "capital_tbl"

    def __unicode__(self):
        return self.excel_input_id

class ApplyCapital(models.Model):
    apply  =  models.ForeignKey(Apply)
    capital =  models.ForeignKey(Capital)
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '预约流水关联表'
        db_table = "apply_capital_tbl"

    def __unicode__(self):
        return str(self.apply)

class ApplyContact(models.Model):
    apply  =  models.ForeignKey(Apply)
    contact = models.ForeignKey(Contact)
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '预约待办关联表'
        db_table = "apply_contact_tbl"

    def __unicode__(self):
        return str(self.apply)

class Documentscan(models.Model):
    # document_id = models.CharField(max_length=256, verbose_name='文件ID')
    document_name = models.CharField(max_length=256, verbose_name='文件文档的名称')
    size = models.IntegerField(verbose_name="文件大小")
    document_type = models.CharField(max_length=256, verbose_name='文件文档的类型')
    content = models.BinaryField(verbose_name='文档内容')
    upload_date = models.CharField(max_length=32, verbose_name='文件文档的类型')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '扫描文件表'
        db_table = "document_scan_tbl"

    def __unicode__(self):
        return self.document_name

class TradeDocument(models.Model):
    document_id   = models.CharField(max_length=32, verbose_name='文件ID')
    trade_id      = models.CharField(max_length=32, verbose_name='交易ID')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '扫描文件及交易关联表'
        db_table = "trade_doc_tbl"

class TradeScan(models.Model):
    trade_id = models.CharField(max_length=32, verbose_name='交易ID')
    object_info = models.CharField(max_length=128, verbose_name='实物存放文件柜')
    object_operator = models.CharField(max_length=50, verbose_name='实物处理人')
    object_date = models.DateTimeField(auto_now_add=True, verbose_name='处理时间')
    created_by    = models.CharField(max_length=50, verbose_name='创建人')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by    = models.CharField(max_length=50, verbose_name='上次修改人')
    updated_date  = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '扫描文件及交易关联表'
        db_table = "trade_scan_tbl"
