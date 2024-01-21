from myApp.models import JobInfo
import json
from .publicData import *

def getPageData():
    jobs = JobInfo.objects.all()
    typesData = []
    for i in jobs:
        typesData.append(i.type)
    return list(set(typesData))
def getCompanyBar(type):
    if type == 'all':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)
    natureData = {}
    for i in jobs:
        if natureData.get(i.companyNature, -1) == -1:
            natureData[i.companyNature] = 1
        else:
            natureData[i.companyNature] += 1
    return list(natureData.keys())[:30], list(natureData.values())[:30]


def getCompanyPie(type):
    if type == 'all':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)
    addressData = {}
    for i in jobs:
        if addressData.get(i.address, -1) == -1:
            addressData[i.address] = 1
        else:
            addressData[i.address] += 1
    result = []
    for key, valye in addressData.items():
        result.append({
            'name': key,
            'value': valye
        })
    return result[:57]


def getCompanPeople(type):
    if type == 'all':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)

    def map_fn(item):
        item.companyPeople = json.loads(item.companyPeople)[1]
        return item

    jobs = list(map(map_fn, jobs))
    data = [0 for x in range(6)]
    for i in jobs:
        p = i.companyPeople
        if p <= 20:
            data[0] += 1
        elif p <= 100:
            data[1] += 1
        elif p <= 500:
            data[2] += 1
        elif p <= 1000:
            data[3] += 1
        elif p < 10000:
            data[4] += 1
        else:
            data[5] += 1
    return companyPeople,data
