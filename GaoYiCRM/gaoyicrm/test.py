__author__ = 'zhangchengyiming'
from django.shortcuts import render

def getmytest(request):
    return render(request,'test.html')