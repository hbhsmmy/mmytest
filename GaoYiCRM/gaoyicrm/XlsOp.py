# -*- coding: UTF-8 -*-
import  xlrd

def ReadFromXlsTable(table, titlenames):
    firstrowindex = -1
    for i in range(0, table.nrows):
        rowval = table.row_values(i)
        if len(rowval) >= len(titlenames):
            for j in (0, len(rowval)):
                if len(rowval[j]) > 0:
                    firstrowindex = i
                    break
        if firstrowindex >= 0:
            break

    firstrow = table.row_values(firstrowindex)
    index = []
    for i in range(0, len(titlenames)):
        for j in range(0, len(firstrow)):
            val = firstrow[j].strip()
            if val == titlenames[i]:
                index.append(j)
                break

    reslist = []
    if len(index) < len(titlenames):
        return reslist

    firstrowindex = firstrowindex + 1
    for i in range(firstrowindex, table.nrows):
        rowval = []
        for j in range(0, len(index)):
            rowval.append(table.cell(i,index[j]).value)
        reslist.append(rowval)

    return reslist







