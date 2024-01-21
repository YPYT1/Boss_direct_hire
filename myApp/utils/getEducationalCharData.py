from .publicData import *
from myApp.models import JobInfo
import json

def getAverged(list):
    result = 0
    for i in list:
        result += i
    return round(result / len(list),2)

def getExpirenceLineData(educational):
    hasEmpty = False
    if educational == '不限':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(educational=educational)
    workExpirences = {'在校/应届':[], '经验不限':[], '1年以内':[], '1-3年':[], '3-5年':[], '5-10年':[], '10年以上':[]}
    workPeople = {'在校/应届':0, '经验不限':0, '1年以内':0, '1-3年':0, '3-5年':0, '5-10年':0, '10年以上':0}
    for job in jobs:
        for k,e in workExpirences.items():
            if job.workExperience == k:
                workExpirences[k].append(json.loads(job.salary)[1])
                workPeople[k] += 1

    for k,e in workExpirences.items():
        try:
            workExpirences[k] = getAverged(e)
        except:
            workExpirences[k] = 0
    if len(jobs) == 0:
        hasEmpty = True
    return educations,list(workExpirences.keys()),list(workExpirences.values()),list(workPeople.values()),hasEmpty

def getEducationsData():
    jobs = JobInfo.objects.all()
    educationData = {}
    for j in jobs:
        if educationData.get(j.educational, -1) == -1:
            educationData[j.educational] = 1
        else:
            educationData[j.educational] += 1
            #{"benkesjia":1,"jshfa":2}
    return list(educationData.keys()),list(educationData.values())
