from .publicData import *
from myApp.models import JobInfo
import json

def getPageData():
    return ['北京','上海','深圳','成都','昆明',"郑州",'重庆','广州','东莞','天津']

def getEducation(address):
    jobs = JobInfo.objects.filter(address=address)
    educationData = {}
    for job in jobs:
        if educationData.get(job.educational,-1) == -1:
            educationData[job.educational] = 1
        else:
            educationData[job.educational] += 1
    result = []
    for k,v in educationData.items():
        result.append({
            "name":k,
            'value':v
        })
    return result

def getDist(address):
    jobs = JobInfo.objects.filter(address=address)
    distData = {}
    for job in jobs:
        if job.dist != '':
            if distData.get(job.dist,-1) == -1:
                distData[job.dist] = 1
            else:
                distData[job.dist] += 1
    result = []
    for k, v in distData.items():
        result.append({
            "name": k,
            'value': v
        })
    return result

def getSalary(address):
    jobs = JobInfo.objects.filter(address=address)
    salaries = []
    for i in jobs:
        if i.pratice == 0:
            salaries.append(json.loads(i.salary)[1])
    salaryColumn = [0 for x in range(len(salaryList))]
    for i in salaries:
        s = i / 1000
        if s < 10:
            salaryColumn[0] += 1
        elif s < 20:
            salaryColumn[1] += 1
        elif s < 30:
            salaryColumn[2] += 1
        elif s < 40:
            salaryColumn[3] += 1
        else:
            salaryColumn[4] += 1
    return salaryList,salaryColumn

def companyPeopleData(address):
    jobs = JobInfo.objects.filter(address=address)
    peoples = []
    for i in jobs:
        peoples.append(json.loads(i.companyPeople)[1])
    peopleColumn = [0 for x in range(len(companyPeople))]
    for p in peoples:
        if p <= 20:
            peopleColumn[0] += 1
        elif p < 100:
            peopleColumn[1] += 1
        elif p < 500:
            peopleColumn[2] += 1
        elif p < 1000:
            peopleColumn[3] += 1
        elif p < 10000:
            peopleColumn[4] += 1
        elif p == 10000:
            peopleColumn[5] += 1
        else:
            peopleColumn[6] += 1
    result = []
    for index,item in enumerate(peopleColumn):
        result.append({
            'name':companyPeople[index],
            'value':item
        })
    return result