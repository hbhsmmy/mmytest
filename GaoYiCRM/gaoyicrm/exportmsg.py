# -*- coding: utf-8 -*-
from xlrd import open_workbook
from xlutils.copy import copy
import xlwt

class ExportInfo:
    def __init__(self):
        self.fundname = ""
        self.fundcode = ""
        self.customertype  = ""
        self.applydate = ""
        self.customername = ""
        self.idtype = ""
        self.idno = ''
        self.bank = ''
        self.bankname = ''
        self.bankaccount = ''
        self.zipcode = ''
        self.mobile = ''
        self.address = ''
        self.money = 0.0
        self.applymoney = 0.0
        self.applytype = ''
        self.shuhui_all = False
        self.shuhui_shares = 0.0
        self.jingban_name = ''
        self.jingban_idtype = ''
        self.jingban_idno = ''
        self.jingban_mobile = ''
        self.faren_name = ''
        self.sheng = ''
        self.shi = ''
        self.daozhang_date = ''
        self.sex = ''
        self.bankaccountname = ''



    def ToGuojinIdType(self):
        if self.customertype == '0':
            if self.idtype == '0':
                return u'组织机构代码'
            elif self.idtype == '1':
                return u'营业执照'
            elif self.idtype == '3':
                return u'社会团体'
            elif self.idtype == '7':
                return u'基金会'
            else:
                return u'其他'
        elif self.customertype == '1':
            if self.idtype == '0':
                return u'身份证'
            elif self.idtype == '1':
                return u'护照'
            elif self.idtype == '5':
                return u'户口本'
            elif self.idtype == '6':
                return u'外国护照'
            elif self.idtype == '4':
                return u'港澳通行证'
            elif self.idtype == 'A':
                return u'台胞证'
            else:
                return u'其他'

    def ToIdName(self):
        if self.customertype == '0':
            if self.idtype == '0':
                return u'组织机构代码证'
            elif self.idtype == '1':
                return u'营业执照'
            elif self.idtype == '2':
                return u'行政机关'
            elif self.idtype == '3':
                return u'社会团体'
            elif self.idtype == '4':
                return u'军队'
            elif self.idtype == '5':
                return u'武警'
            elif self.idtype == '6':
                return u'下属机构'
            elif self.idtype == '7':
                return u'基金会'
            elif self.idtype == '8':
                return u'其他'
            else:
                return u'其他'
        elif self.customertype == '1':
            if self.idtype == '0':
                return u'身份证'
            elif self.idtype == '5':
                return u'户口本'
            elif self.idtype == '2':
                return u'军官证'
            elif self.idtype == '4':
                return u'港澳居民来往内地通行'
            elif self.idtype == '1':
                return u'护照'
            elif self.idtype == '3':
                return u'士兵证'
            elif self.idtype == '6':
                return u'外国护照'
            elif self.idtype == '7':
                return u'其他'
            elif self.idtype == '8':
                return u'文职证'
            elif self.idtype == '9':
                return u'警官证'
            elif self.idtype == 'A':
                return u'台胞证'
            else:
                return u'其他'

def copyXF(rdbook,rdxf):
    """
    clone a XFstyle from xlrd XF class,the code is copied from xlutils.copy module
    """

    wtxf = xlwt.Style.XFStyle()
    #
    # number format
    #
    wtxf.num_format_str = rdbook.format_map[rdxf.format_key].format_str
    #
    # font
    #
    wtf = wtxf.font
    rdf = rdbook.font_list[rdxf.font_index]
    wtf.height = rdf.height
    wtf.italic = rdf.italic
    wtf.struck_out = rdf.struck_out
    wtf.outline = rdf.outline
    wtf.shadow = rdf.outline
    wtf.colour_index = rdf.colour_index
    wtf.bold = rdf.bold #### This attribute is redundant, should be driven by weight
    wtf._weight = rdf.weight #### Why "private"?
    wtf.escapement = rdf.escapement
    wtf.underline = rdf.underline_type ####
    # wtf.???? = rdf.underline #### redundant attribute, set on the fly when writing
    wtf.family = rdf.family
    wtf.charset = rdf.character_set
    wtf.name = rdf.name
    #
    # protection
    #
    wtp = wtxf.protection
    rdp = rdxf.protection
    wtp.cell_locked = rdp.cell_locked
    wtp.formula_hidden = rdp.formula_hidden
    #
    # border(s) (rename ????)
    #
    wtb = wtxf.borders
    rdb = rdxf.border
    wtb.left   = rdb.left_line_style
    wtb.right  = rdb.right_line_style
    wtb.top    = rdb.top_line_style
    wtb.bottom = rdb.bottom_line_style
    wtb.diag   = rdb.diag_line_style
    wtb.left_colour   = rdb.left_colour_index
    wtb.right_colour  = rdb.right_colour_index
    wtb.top_colour    = rdb.top_colour_index
    wtb.bottom_colour = rdb.bottom_colour_index
    wtb.diag_colour   = rdb.diag_colour_index
    wtb.need_diag1 = rdb.diag_down
    wtb.need_diag2 = rdb.diag_up
    #
    # background / pattern (rename???)
    #
    wtpat = wtxf.pattern
    rdbg = rdxf.background
    wtpat.pattern = rdbg.fill_pattern
    wtpat.pattern_fore_colour = rdbg.pattern_colour_index
    wtpat.pattern_back_colour = rdbg.background_colour_index
    #
    # alignment
    #
    wta = wtxf.alignment
    rda = rdxf.alignment
    wta.horz = rda.hor_align
    wta.vert = rda.vert_align
    wta.dire = rda.text_direction
    # wta.orie # orientation doesn't occur in BIFF8! Superceded by rotation ("rota").
    wta.rota = rda.rotation
    wta.wrap = rda.text_wrapped
    wta.shri = rda.shrink_to_fit
    wta.inde = rda.indent_level
    # wta.merg = ????
    #
    return wtxf

def WriteXlsCell(rsbook,ws, rs, row, col, data):
    xfx = rs.cell_xf_index(row, col)
    xf = rsbook.xf_list[xfx]
    xfstyle = copyXF(rsbook, xf)
    ws.write(row, col, data, xfstyle)

def ExportToGuojin(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws_sg = wb.get_sheet(0)
    ws_sh = wb.get_sheet(1)
    ishengou = 4
    ishuhui = 4
    for v in appinfos:
        if v.applytype == '1' or v.applytype == '2':
            WriteXlsCell(rb, ws_sg, rs, 1, 1, v.fundname)
            WriteXlsCell(rb, ws_sg, rs, 2, 1, v.fundcode)
            if v.customertype == "1":
                WriteXlsCell(rb, ws_sg, rs, ishengou, 0, u'否')
            else:
                WriteXlsCell(rb, ws_sg, rs, ishengou, 0, u'是')
            WriteXlsCell(rb, ws_sg, rs, ishengou, 1, v.applydate)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 2, v.customername)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 3, v.ToGuojinIdType())
            WriteXlsCell(rb, ws_sg, rs, ishengou, 4, v.idno)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 5, v.bank)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 6, v.customername)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 7, v.bankaccount)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 8, v.zipcode)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 9, v.mobile)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 10, v.address)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 11, v.money)
            WriteXlsCell(rb, ws_sg, rs, ishengou, 13, v.applymoney)
            if v.applytype == '1':
                WriteXlsCell(rb, ws_sg, rs, ishengou, 14, u"认购")
            else:
                WriteXlsCell(rb, ws_sg, rs, ishengou, 14, u"申购")
            ishengou = ishengou + 1
        elif v.applytype == '3':
            WriteXlsCell(rb, ws_sh, rs, 1, 1, v.fundname)
            WriteXlsCell(rb, ws_sh, rs, 2, 1, v.fundcode)
            WriteXlsCell(rb, ws_sh, rs, ishuhui, 1, v.applydate)
            WriteXlsCell(rb, ws_sh, rs, ishuhui, 2, v.customername)
            WriteXlsCell(rb, ws_sh, rs, ishuhui, 3, v.ToGuojinIdType())
            WriteXlsCell(rb, ws_sh, rs, ishuhui, 4, v.idno)
            if v.shuhui_all:
                WriteXlsCell(rb, ws_sh, rs, ishuhui, 5, u'全部份额')
            else:
                WriteXlsCell(rb, ws_sh, rs, ishuhui, 5, v.shuhui_shares)
            WriteXlsCell(rb, ws_sh, rs, ishuhui, 6, u"继续赎回")
            ishuhui = ishuhui + 1

    wb.save(outfilename)

def ExportToGuoXin(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    i = 4
    for v in appinfos:
        WriteXlsCell(rb, ws, rs, i, 0, v.applydate)
        WriteXlsCell(rb, ws, rs, i, 1, v.fundname)
        WriteXlsCell(rb, ws, rs, i, 2, v.money)
        WriteXlsCell(rb, ws, rs, i, 3, v.customername)
        if v.applytype == '1':
            WriteXlsCell(rb, ws, rs, i, 4, u'认购')
        elif v.applytype == '2':
            WriteXlsCell(rb, ws, rs, i, 4, u'申购')
        elif v.applytype == '3':
            WriteXlsCell(rb, ws, rs, i, 4, u'赎回')
            WriteXlsCell(rb, ws, rs, i, 5, v.shuhui_shares)
        WriteXlsCell(rb, ws, rs, i, 6, 0)
        WriteXlsCell(rb, ws, rs, i, 7, v.ToIdName())
        WriteXlsCell(rb, ws, rs, i, 8, v.idno)
        WriteXlsCell(rb, ws, rs, i, 9, v.bankaccount)
        WriteXlsCell(rb, ws, rs, i, 10, v.bank)
        i = i + 1
    wb.save(outfilename)

def ExportToCMB(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    i = 4
    for v in appinfos:
        WriteXlsCell(rb, ws, rs, i, 0, v.customername)
        if v.customertype == '0':
            WriteXlsCell(rb, ws, rs, i, 1, u'0|机构')
            WriteXlsCell(rb, ws, rs, i, 2, v.idtype + '|' + u'（机构）' + v.ToIdName())
        elif v.customertype == '1':
            WriteXlsCell(rb, ws, rs, i, 1, u'0|个人')
            WriteXlsCell(rb, ws, rs, i, 2, v.idtype + '|' + u'（个人）' + v.ToIdName())
        WriteXlsCell(rb, ws, rs, i, 3, v.idno)
        WriteXlsCell(rb, ws, rs, i, 7, v.fundcode)
        if v.applytype == '1':
            WriteXlsCell(rb, ws, rs, i, 8, u'20|认购')
            WriteXlsCell(rb, ws, rs, i, 9, v.money)
        elif v.applytype == '2':
            WriteXlsCell(rb, ws, rs, i, 8, u'22|申购')
            WriteXlsCell(rb, ws, rs, i, 9, v.money)
        elif v.applytype == '3':
            WriteXlsCell(rb, ws, rs, i, 8, u'24|赎回')
            WriteXlsCell(rb, ws, rs, i, 10, v.shuhui_shares)
        WriteXlsCell(rb, ws, rs, i, 11, v.applydate)
        WriteXlsCell(rb, ws, rs, i, 12, u'0|成年人')
        WriteXlsCell(rb, ws, rs, i, 16, u'0.0')
        i = i + 1
    wb.save(outfilename)

def ExportToCMS_shengou(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    i = 1
    for v in appinfos:
        WriteXlsCell(rb, ws, rs, i, 0, i)
        WriteXlsCell(rb, ws, rs, i, 1, v.customername)
        WriteXlsCell(rb, ws, rs, i, 2, v.money / 10000)
        if v.customertype == '0':
            WriteXlsCell(rb, ws, rs, i, 3, u'机构')
            WriteXlsCell(rb, ws, rs, i, 6, v.jingban_name)
            WriteXlsCell(rb, ws, rs, i, 7, v.faren_name)
        elif v.customertype == '1':
            WriteXlsCell(rb, ws, rs, i, 3, u'个人')
            WriteXlsCell(rb, ws, rs, i, 7, v.customername)
        WriteXlsCell(rb, ws, rs, i, 4, v.ToIdName())
        WriteXlsCell(rb, ws, rs, i, 5, v.idno)
        WriteXlsCell(rb, ws, rs, i, 8, v.bankaccount)
        WriteXlsCell(rb, ws, rs, i, 9, v.customername)
        WriteXlsCell(rb, ws, rs, i, 10, v.bank)
        WriteXlsCell(rb, ws, rs, i, 11, v.sheng)
        WriteXlsCell(rb, ws, rs, i, 11, v.shi)
        i = i + 1
    wb.save(outfilename)

def ExportToCMS_shuhui(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    i = 1
    for v in appinfos:
        WriteXlsCell(rb, ws, rs, i, 0, i)
        WriteXlsCell(rb, ws, rs, i, 1, v.customername)
        if v.customertype == '0':
            WriteXlsCell(rb, ws, rs, i, 2, u'机构')
        elif v.customertype == '1':
            WriteXlsCell(rb, ws, rs, i, 2, u'个人')
        WriteXlsCell(rb, ws, rs, i, 3, v.ToIdName())
        WriteXlsCell(rb, ws, rs, i, 4, v.idno)
        WriteXlsCell(rb, ws, rs, i, 5, v.shuhui_shares)
        i = i + 1
    wb.save(outfilename)

def ExportToCMS(shengou_file, shuhui_file, out_shengou_file, out_shuhui_file, appinfos):
    shengou = []
    shuhui = []
    for v in appinfos:
        if v.applytype == '3':
            shuhui.append(v)
        else:
            shengou.append(v)
    ExportToCMS_shengou(shengou_file, out_shengou_file, shengou)
    ExportToCMS_shuhui(shuhui_file, out_shuhui_file, shuhui)

def ExportToCITIC(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    WriteXlsCell(rb, ws, rs, 3, 1, u' 基金编码：' + appinfos[0].fundcode)
    WriteXlsCell(rb, ws, rs, 4, 1, u' 基金名称：' + appinfos[0].fundname)
    i = 6
    for v in appinfos:
        WriteXlsCell(rb, ws, rs, i, 1, i - 5)
        if v.applytype == '3':
            WriteXlsCell(rb, ws, rs, i, 2, u'□认购/申购'+'     '+u'√赎回')
            WriteXlsCell(rb, ws, rs, i, 10, v.shuhui_shares)
        else:
            WriteXlsCell(rb, ws, rs, i, 2, u'√认购/申购'+ '     '+u'□赎回')
            WriteXlsCell(rb, ws, rs, i, 9, v.money / 10000)
        WriteXlsCell(rb, ws, rs, i, 4, v.customername)
        WriteXlsCell(rb, ws, rs, i, 5, v.ToIdName())
        WriteXlsCell(rb, ws, rs, i, 6, v.idno)
        WriteXlsCell(rb, ws, rs, i, 7, v.applydate)
        WriteXlsCell(rb, ws, rs, i, 11, v.daozhang_date)
        i = i + 1
    wb.save(outfilename)

def ExportToCITICOpenAccount(guojin_file, outfilename, appinfos):
    if len(appinfos) <= 0:
        return
    rb = open_workbook(guojin_file, formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    i = 2
    for v in appinfos:
        #ws.write(i, 0, i - 1)
        WriteXlsCell(rb, ws, rs, i, 0, i - 1)
        if v.customertype == '0':
            WriteXlsCell(rb, ws, rs, i, 1, u'机构')
            WriteXlsCell(rb, ws, rs, i, 8, v.jingban_mobile)
            WriteXlsCell(rb, ws, rs, i, 10, v.jingban_name)
            if v.jingban_idtype == '0':
                WriteXlsCell(rb, ws, rs, i, 11, u'身份证')
            elif v.jingban_idtype == '1':
                WriteXlsCell(rb, ws, rs, i, 11, u'外国护照')
            WriteXlsCell(rb, ws, rs, i, 12, v.jingban_idno)
        elif v.customertype == '1':
            WriteXlsCell(rb, ws, rs, i, 1, u'个人')
            WriteXlsCell(rb, ws, rs, i, 7, v.sex)
            WriteXlsCell(rb, ws, rs, i, 8, v.mobile)
        WriteXlsCell(rb, ws, rs, i, 3, v.customername)
        WriteXlsCell(rb, ws, rs, i, 5, v.ToIdName())
        WriteXlsCell(rb, ws, rs, i, 6, v.idno)
        WriteXlsCell(rb, ws, rs, i, 9, v.address)
        WriteXlsCell(rb, ws, rs, i, 13, v.bankaccountname)
        WriteXlsCell(rb, ws, rs, i,14, v.bankaccount)
        WriteXlsCell(rb, ws, rs, i, 15, v.bank)
        i = i + 1
    wb.save(outfilename)
