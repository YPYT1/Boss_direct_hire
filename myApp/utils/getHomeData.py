from myApp.models import User, JobInfo
from .publicData import *
import time
import json
import re


# 首页时间+欢迎语
def getNowTime():
    timeFormat = time.localtime()
    year = timeFormat.tm_year
    month = timeFormat.tm_mon
    day = timeFormat.tm_mday
    monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "December"]
    return year, monthList[month - 1], day


# 首页右侧7指标
def getTagData():
    jobs = getAllJobInfo()
    users = getAllUser()
    educationsTop = "学历不限"
    salaryTop = 0
    salaryMonthTop = 0
    address = {}
    pratice = {}

    # Preprocessing salaries and salary months for non-practise jobs
    preprocessed_salaries = [(clean_salary(json.loads(job.salary)[1]), job) for job in jobs if not job.pratice and len(json.loads(job.salary)) > 1 and isinstance(json.loads(job.salary)[1], str)]
    preprocessed_salary_months = [(clean_salary(job.salaryMonth), job) for job in jobs]

    # Finding the top non-practise salary
    if preprocessed_salaries:
        salaryTop = max(preprocessed_salaries, key=lambda x: x[0])[0]

    # Finding the top salary month
    if preprocessed_salary_months:
        salaryMonthTop = max(preprocessed_salary_months, key=lambda x: x[0])[0]

    # Process for educational level and counting addresses and practice types
    for job in jobs:
        job_education_value = educations.get(job.educational, 9)  # Assuming 9 is the default value
        if job_education_value < educations.get(educationsTop, 9):
            educationsTop = job.educational

        # Counting occurrences of address
        address[job.address] = address.get(job.address, 0) + 1

        # Counting occurrences of practice type
        pratice[job.pratice] = pratice.get(job.pratice, 0) + 1

    # Finding top 3 addresses
    addressStr = sorted(address.items(), key=lambda x: x[1], reverse=True)[:3]
    addressTop = ",".join([i[0] for i in addressStr])

    # Finding the most common practice type
    praticeMax = max(pratice.items(), key=lambda x: x[1])
    a = "普通岗位" if not praticeMax[0] else "实习岗位"

    return len(jobs), len(users), educationsTop, salaryTop, salaryMonthTop, addressTop, a
# 用户创建时间饼状图
def getUserCreateTime():
    users = getAllUser()
    data = {}
    for u in users:
        if data.get(str(u.createTime), -1) == -1:
            data[str(u.createTime)] = 1
        else:
            data[str(u.createTime)] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return result


def getUserTop5():
    users = getAllUser()

    def sort_fn(item):
        return time.mktime(time.strptime(str(item.createTime), '%Y-%m-%d'))

    users = list(sorted(users, key=sort_fn, reverse=True))[:6]
    return users


def getTableData():
    jobs = getAllJobInfo()
    for i in jobs:
        i.workTag = '/'.join(json.loads(i.workTag))
        if i.companyTags != "无":
            i.companyTags = '/'.join(json.loads(i.companyTags))

        i.companyPeople = json.loads(i.companyPeople)
        i.companyPeople = list(map(lambda x: str(x) + '人', i.companyPeople))
        i.companyPeople = '-'.join(i.companyPeople)
        i.salary = json.loads(i.salary)[1]
    return jobs
    # jobs[0].workTags = '/'.join(json.loads(jobs[0].workTag))
    # def map_fn(item):
    #     item.workTag = "/".join()
    # jobs = list(map(map_fn,jobs))


# 辅助函数
def clean_salary(salary_str):
    # 使用正则表达式移除非数字字符
    cleaned_str = re.sub(r'[^\d]', '', salary_str)
    # 转换为整数
    return int(cleaned_str) if cleaned_str else 0
