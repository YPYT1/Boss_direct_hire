from .publicData import *
from myApp.models import JobInfo
import json

def getPageData():
    return list(educations.keys()), workExpirences
def getBarData(educational, workExpirence):
    salaryList = ['0-10k', '10-20k', '20-30k', '30-40k', '40k以上']
    if educational == '不限' and workExpirence == '不限':
        jobs = JobInfo.objects.all()
    elif workExpirence == '不限':
        jobs = JobInfo.objects.filter(educational=educational)
    elif educational == '不限':
        jobs = JobInfo.objects.filter(workExperience=workExpirence)
    else:
        jobs = JobInfo.objects.filter(educational=educational, workExperience=workExpirence)
    jobsType = {}
    for j in jobs:
        if j.pratice == 0:
            if jobsType.get(j.type, -1) == -1:
                # {Java：[1000,245646,4666,3646,5]}
                jobsType[j.type] = [json.loads(j.salary)[1]]
            else:
                jobsType[j.type].append(json.loads(j.salary)[1])
    barData = {}
    for k, v in jobsType.items():
        if not barData.get(k, 0):
            barData[k] = [0 for x in range(5)]
        for i in v:
            s = i / 1000
            if s < 10:
                barData[k][0] += 1
            elif s >= 10 and s < 20:
                barData[k][1] += 1
            elif s >= 20 and s < 30:
                barData[k][2] += 1
            elif s >= 30 and s < 40:
                barData[k][3] += 1
            else:
                barData[k][4] += 1
    legend = list(barData.keys())
# {java:}
    if len(legend) == 0:
        legend = None
    return salaryList, barData, list(barData.keys())

def addList(list):
    total = 0
    for i in list:
        total += i
    return round(total / len(list), 1)


def pieData():
    jobs = JobInfo.objects.all()
    jobsType = {}
    for j in jobs:
        if j.pratice == 1:
            if jobsType.get(j.type, -1) == -1:
                jobsType[j.type] = [json.loads(j.salary)[1]]
            else:
                jobsType[j.type].append(json.loads(j.salary)[1])
    result = []
    for k, v in jobsType.items():
        result.append({
            'name': k,
            'value': addList(v)
        })
    return result


def louDouData():
    jobs = JobInfo.objects.filter(salaryMonth__gt=0)
    data = {}
    for j in jobs:
        x = str(j.salaryMonth) + '薪'
        if data.get(x, -1) == -1:
            data[x] = 1
        else:
            data[x] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return list(data.keys()), result

