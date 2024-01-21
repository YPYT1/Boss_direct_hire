import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
import hashlib

from django.views.decorators.csrf import csrf_protect

from .models import *
from .error import *
from myApp.models import JobInfo, User
from .utils import getHomeData
from .utils import getSelfInfoData
from .utils import getChangePassword
from .utils import getHistoryTableData
from .utils import getTableData
from .utils import getSalaryCharData
from .utils import getCompanyCharData
from .utils import getEducationalCharData
from .utils import getCompanyStatusCharData
from .utils import getAddressCharData
from word_cloud_picture import *
import random


# 登录页面
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pwd.encode())
        pwd = md5.hexdigest()
        try:
            user = User.objects.get(username=uname, password=pwd)
            request.session['username'] = user.username
            return redirect('home')
        except:
            return errorResponse(request, '用户名或密码错误!')


# 注册页面
def registry(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        checkPWD = request.POST.get('checkPassword')
        try:
            User.objects.get(username=uname)
        except:
            if not uname or not pwd or not checkPWD: return errorResponse(request, '不允许为空!')
            if pwd != checkPWD: return errorResponse(request, '两次密码不符合!')
            md5 = hashlib.md5()
            md5.update(pwd.encode())
            pwd = md5.hexdigest()
            User.objects.create(username=uname, password=pwd)
            return redirect('login')
        return errorResponse(request, '该用户已被注册')


# 退出登录
def logOut(request):
    request.session.clear()
    return redirect('login')


# 首页
def home(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    year, month, day = getHomeData.getNowTime()
    jobsLen, usersLen, educationsTop, salaryTop, salaryMonthTop, addressTop, praticeMax = getHomeData.getTagData()
    userTime = getHomeData.getUserCreateTime()
    newUser = getHomeData.getUserTop5()
    # allJobsPBar = getHomeData.getAllJobsPBar()
    tableData = getHomeData.getTableData()
    return render(request, 'index.html', {
        'username': username,
        'userAvatar': userInfo.avatar,
        'year': year,
        "month": month,
        'day': day,
        'jobsLen': jobsLen,
        'usersLen': usersLen,
        'educationsTop': educationsTop,
        'salaryTop': salaryTop,
        'salaryMonthTop': salaryMonthTop,
        'praticeMax': praticeMax,
        'addressTop': addressTop,
        'userTime': userTime,
        'newUser': newUser,
        'tableData': tableData
    })


# 个人信息页面
# def selfInfo(request):
#     username = request.session.get("username")
#     userInfo = User.objects.get(username=username)
#     educations,workExperience,jobsTypes = getSelfInfoData.getPageData()
#     if request.method == 'GET':
#         return render(request,'selfInfo.html',{
#             'username': username,
#             'userInfo': userInfo,
#             'educations':educations,
#             'workExperience':workExperience,
#             'jobsTypes':jobsTypes
#         })
#     else:
#         getSelfInfoData.changeSelfInfo(request.POST,request.FILES)
#         userInfo = User.objects.get(username=username)
#         return render(request, 'selfInfo.html', {
#             'username': username,
#             'userInfo': userInfo,
#             'educations': educations,
#             'workExperience': workExperience,
#             'jobsTypes': jobsTypes
#         })
# 个人信息页面
def selfInfo(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    educations, workExperience, jobsTypes = getSelfInfoData.getPageData()

    if request.method == 'GET':
        return render(request, 'selfInfo.html', {
            'username': username,
            'userInfo': userInfo,
            'educations': educations,
            'workExperience': workExperience,
            'jobsTypes': jobsTypes
        })
    else:
        newInfo = request.POST
        FileInfo = request.FILES

        # 确保所有表单字段都已填写，如果图片未上传，则提示消息
        mandatory_fields = ['username', 'educational', 'workExpirence', 'address', 'work']
        missing_fields = [field for field in mandatory_fields if not newInfo.get(field)]
        if missing_fields or ('avatar' not in FileInfo):
            messages.error(request, '请填写所有信息，包括上传图片。')
        else:
            getSelfInfoData.changeSelfInfo(newInfo, FileInfo)

        # 无论是否成功更新，都重新获取userInfo用于显示
        userInfo = User.objects.get(username=username)
        return render(request, 'selfInfo.html', {
            'username': username,
            'userInfo': userInfo,
            'educations': educations,
            'workExperience': workExperience,
            'jobsTypes': jobsTypes
        })


# 修改密码页
def changePassword(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    if request.method == 'GET':
        return render(request, 'changePassword.html', {
            'username': username,
            'userInfo': userInfo,
        })
    else:
        res = getChangePassword.changePassword(request.POST, userInfo)
        if res != None:
            return render(request, 'error.html', {
                'errorMsg': res
            })
        userInfo = User.objects.get(username=username)
        return render(request, 'changePassword.html', {
            'username': username,
            'userInfo': userInfo,
        })


# 数据统计页
def tableData(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    tableData = getTableData.getTableData()
    paginator = Paginator(tableData, 10)
    # 根据请求地址的信息来跳转页码数据
    cur_page = 1
    if request.GET.get("page"):
        cur_page = int(request.GET.get("page"))
    if cur_page:
        c_page = paginator.page(cur_page)
    else:
        c_page = paginator.page(1)

    page_range = []
    visibleNumber = 15
    min = int(cur_page - visibleNumber / 2)
    if min < 1:
        min = 1
    max = min + visibleNumber
    if max > paginator.page_range[-1]:
        max = paginator.page_range[-1]
    for i in range(min, max):
        page_range.append(i)

    return render(request, 'tableData.html', {
        'username': username,
        'userInfo': userInfo,
        'tableData': tableData,
        "pagination": paginator,
        "c_page": c_page,
        'page_range': page_range
    })


# 岗位收藏
def historyTableData(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    historyData = getHistoryTableData.getHistoryData(userInfo)
    return render(request, 'historyTableData.html', {
        'userInfo': userInfo,
        'historyData': historyData
    })


# 添加历史
def addHistory(request, jobId):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    getHistoryTableData.addHistory(userInfo, jobId)
    return redirect('historyTableData')


# 删除历史
def removeHistory(request, hisId):
    getHistoryTableData.removeHistory(hisId)
    return redirect('historyTableData')


# 薪资情况
def salary(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    # 选择框
    educations, workExpirences = getSalaryCharData.getPageData()
    defaultEducation = '不限'
    defaultWorkExpirence = '不限'
    if request.GET.get("educational"): defaultEducation = request.GET.get("educational")
    if request.GET.get("workExpirence"): defaultWorkExpirence = request.GET.get("workExpirence")
    salaryList, barData, legend = getSalaryCharData.getBarData(defaultEducation, defaultWorkExpirence)
    pieData = getSalaryCharData.pieData()
    loudouLegend, louDouData = getSalaryCharData.louDouData()
    return render(request, 'salaryChart.html', {
        'userInfo': userInfo,
        'educations': educations,
        'workExpirences': workExpirences,
        'defaultEducation': defaultEducation,
        'defaultWorkExpirence': defaultWorkExpirence,
        'salaryList': salaryList,
        'barData': barData,
        'legend': legend,
        'pieData': pieData,
        'loudouLegend': loudouLegend,
        'louDouData': louDouData
    })


# 公司情况
def company(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    type = 'all'
    if request.GET.get("type"): type = request.GET.get("type")
    typeList = getCompanyCharData.getPageData()
    natureRow, natureColumn = getCompanyCharData.getCompanyBar(type)
    addressData = getCompanyCharData.getCompanyPie(type)
    companyPeopleXData, companyPeopleYData = getCompanyCharData.getCompanPeople(type)
    return render(request, 'companyChart.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'type': type,
        'natureRow': natureRow,
        'natureColumn': natureColumn,
        'addressData': addressData,
        'companyPeopleXData': companyPeopleXData,
        'companyPeopleYData': companyPeopleYData
    })


# 福利词云图
def companyTags(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    return render(request, 'companyTagsWord_cloud.html', {
        "userInfo": userInfo
    })


# 学历情况
def educational(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    defaultEducation = '不限'
    if request.GET.get("educational"): defaultEducation = request.GET.get("educational")
    educations, charDataRow, chrDataColumn1, chrDataColumn2, hasEmpty = getEducationalCharData.getExpirenceLineData(
        defaultEducation)
    educationsDataRow, educationsDataColumn = getEducationalCharData.getEducationsData()
    return render(request, 'educationalChat.html', {
        "userInfo": userInfo,
        'educations': educations,
        'defaultEducation': defaultEducation,
        'charDataRow': charDataRow,
        'chrDataColumn1': chrDataColumn1,
        'chrDataColumn2': chrDataColumn2,
        "hasEmpty": hasEmpty,
        'educationsDataRow': educationsDataRow,
        'educationsDataColumn': educationsDataColumn
    })


# 模型预测
def yuce(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)

    return render(request, 'yuce.html', {
        "userInfo": userInfo
    })


# 企业融资
def companyStatus(request):
    username = request.session.get("username")
    userInfo = User.objects.get(username=username)
    defaultType = '不限'
    if request.GET.get("type"): defaultType = request.GET.get("type")
    statusData = getCompanyStatusCharData.getCompanyStatusData()
    typeList = getCompanyStatusCharData.getPageData()
    TeachnologyDataRow, TeachnologyDataColumn = getCompanyStatusCharData.getTeachnologyData(defaultType)
    return render(request, 'companyStatus.html', {
        'userInfo': userInfo,
        'statusData': statusData,
        'typeList': typeList,
        'defaultType': defaultType,
        'TeachnologyDataRow': TeachnologyDataRow,
        'TeachnologyDataColumn': TeachnologyDataColumn
    })
