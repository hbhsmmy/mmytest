# -*- coding: UTF-8 -*-
import  xlrd
import  time
import datetime
import MySQLdb
from XlsOp import *

# xwmysqlhost = '115.159.154.36'
# xwmysqluser = 'root'
# xwmysqlpwd = 'Gaoyi001'
#
# frhost = '115.159.154.36'
# fruser = 'root'
# frpwd = 'Gaoyi001'
# frdatabase = 'fund_report'
#
# crmhost = '115.159.154.36'
# crmuser = 'root'
# crmpwd = 'Gaoyi001'
# crmdb = 'crmdata'
#
xwmysqlhost = '10.25.16.2'
xwmysqluser = 'crmadmin'
xwmysqlpwd = 'i7ulWHv6'

frhost = '10.25.16.2'
fruser = 'webadmin'
frpwd = 'sIXob8v1'
frdatabase = 'fund_report'

crmhost = '10.25.16.2'
crmuser = 'crmadmin'
crmpwd = 'i7ulWHv6'
crmdb = 'gycrmdb'

class Capital:
    def __init__(self):
        self.inputid = 0  #记账流水号
        self.fundid = ""
        #self.fundaccount = "" #基金收款帐号
        self.capitaltime = "" #资金流水时间
        self.payeename = ""   # 客户付款账户名
        self.payeeaccount = "" #客户付款账号
        self.paysum = 0.0      #贷方金额，使用该金额匹配
        self.viraccount = ""  #招证-虚拟编号
        self.virname = ""  #招证-虚拟户户名
        self.note = ""  #备注


def GetFundIdFromFundInfo(fundname, wxhost, wxuser, wxpwd):
    db = MySQLdb.connect(wxhost, wxuser, wxpwd, 'wxdata', charset='utf8')
    cursor = db.cursor()
    sql = "select id from fund_info where fund_name = '" + fundname + "' and delete_flag = 0"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            return row[0]
    except:
        print sql
    cursor.close()
    db.close()
    return ''

def GetFundIdFromMapTable(fundname, mysqlhost, mysqluser, mysqlpwd, databasename):
    db = MySQLdb.connect(mysqlhost, mysqluser, mysqlpwd, databasename, charset='utf8')
    cursor = db.cursor()
    sql = "SELECT fund_id from excel_fund_name_tbl where excel_fund_name = '" + fundname + "';"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            return row[0]
    except:
        print sql
    cursor.close()
    db.close()
    return ''

def GetTimeFromValue(ftime):
    if type(ftime) == float:
        strtime = str(ftime)[:8]
        return strtime + " 00:00:00"
        #return str(datetime.datetime.localtime(ftime))
        #return datetime.datetime.strftime('%Y%m%d', str)
    timestr = ftime.strip()
    if len(timestr) < 16:
        timestr = timestr[0:8]
        return str(datetime.datetime.strptime(timestr, "%Y%m%d"))
    return str(datetime.datetime.strptime(timestr, "%Y%m%d %H:%M:%S"))

def ReadFromXls(filename):
    alldata = xlrd.open_workbook(filename)
    table = alldata.sheet_by_index(0)
    headerlist = [u'交易日期', u'交易时间', u'贷', u'收付方账号', u'交易摘要', u'虚拟户编号', u'虚拟户户名', u'记账流水号', u'收付方名称']
    reslist = ReadFromXlsTable(table,headerlist)
    capitallist = []
    if len(reslist) > 0:
        for i in range(0, len(reslist)):
            print reslist[i]
            print reslist[i][4].encode('utf-8')
            #for v in reslist[i]:
            #    print v
            if str(reslist[i][2]) != '' and reslist[i][2] > 0.0001:
                item = Capital()
                #floatstr = str(reslist[i][0]).strip()
                #floatval = float(floatstr)
                #realstr = floatstr
                #if floatval < 19000000:
                #    realstr = datetime.datetime.strftime('%Y%m%d', datetime.datetime.localtime(floatval))
                    #dotstr = '.'
                    #nPos = realstr.index(dotstr)
                #    print  realstr
                #    realstr = realstr[:-3]
                #    print  realstr
                #print  realstr

                dt = GetTimeFromValue(reslist[i][0])

                print type(dt)
                timestr = dt[:10] + ' ' + reslist[i][1].strip()
                #dt = datetime.datetime.strptime(timestr, "%Y%m%d %H:%M:%S")
                item.capitaltime = timestr
                #item.paysum = reslist[i][2]
                if type(reslist[i][5]) == float:
                    item.paysum = reslist[i][5]
                else:
                    tmpstr = reslist[i][5]
                    tmpstr = tmpstr.replace(',', '')
                    item.paysum = float(tmpstr)
                if type(reslist[i][3]) == float:
                    item.payeeaccount = str(reslist[i][3]).strip()
                else:
                    item.payeeaccount = reslist[i][3].strip()
                item.note = reslist[i][4].strip()
                item.viraccount = reslist[i][5].strip()
                item.virname = reslist[i][6].strip()
                item.inputid = reslist[i][7].strip()
                item.payeename = reslist[i][8].strip()
                item.fundid = GetFundIdFromFundInfo(item.virname, xwmysqlhost, xwmysqluser, xwmysqlpwd)
                capitallist.append(item)
    else:
        headerlist = [u'编号', u'产品名称', u'户名', u'卡号', u'交易时间', u'缴款金额', u'摘要']
        reslist = ReadFromXlsTable(table,headerlist)
        for i in range(0, len(reslist)):
            item = Capital()
            item.inputid = str(int(reslist[i][0])).strip()
            item.virname = reslist[i][1].strip()
            item.payeename = reslist[i][2].strip()
            item.payeeaccount = reslist[i][3].strip()
            #item.capitaltime = reslist[i][4].strip()
            item.capitaltime = GetTimeFromValue(reslist[i][4])
            if type(reslist[i][5]) == float:
                item.paysum = reslist[i][5]
            else:
                tmpstr = reslist[i][5]
                tmpstr = tmpstr.replace(',', '')
                item.paysum = float(tmpstr)
            item.note = reslist[i][6]
            item.fundid = GetFundIdFromFundInfo(item.virname, xwmysqlhost, xwmysqluser, xwmysqlpwd)
            if str(item.fundid) == '':
                item.fundid = GetFundIdFromMapTable(item.virname, frhost, fruser, frpwd, frdatabase)
            capitallist.append(item)
    return capitallist

def WriteToMysql(capitallist, host, usr, pwd, database):
    db = MySQLdb.connect(host, usr, pwd, database, charset='utf8')
    cursor = db.cursor()
    sql = ''
    date=datetime.datetime.now()
    strnow =date.strftime("%Y-%m-%d %H:%M:%S")
    try:
        for v in capitallist:
            #sql = "insert into capital_tbl(excel_input_id, fund_id, capital_date, payee_account_name, payee_account_no, credit_sum, vir_account_no, vir_account_name, note, status, created_by, created_date, updated_by, updated_date) values ('" + v.inputid + "', '" + v.fundid + "','" + v.capitaltime + "', '" + v.payeename + "','" + v.payeeaccount + "'," + v.paysum + ", '" + v.viraccount + "', '" + v.virname + "','" + v.note + "','1', 'sys','" + strnow + "', 'sys', '" + strnow + "');"
            print type(v.paysum)
            #v.paysum = v.paysum.replace(',', '')
            sql = "insert into capital_tbl(excel_input_id, fund_id, capital_date, payee_account_name, payee_account_no, credit_sum, vir_account_no, vir_account_name, note, status, created_by, created_date, updated_by, updated_date) values ('"\
                   + v.inputid  + "', '" + v.fundid + "','" + str(v.capitaltime) + "', '" + v.payeename + "','" + v.payeeaccount + "'," + str(v.paysum) + ", '" + v.viraccount + "', '" + v.virname + "','" + v.note + "','1', 'sys','" + strnow + "', 'sys', '" + strnow + "');"
            cursor.execute(sql)
        db.commit()
    except:
        print sql
    cursor.close()
    db.close()


def XlsToMysql(filename):
    reslist = ReadFromXls(filename)
    WriteToMysql(reslist, crmhost, crmuser, crmpwd, crmdb)

# XlsToMysql(u"E:/tmp/test2016.xls")