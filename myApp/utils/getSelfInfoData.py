from .publicData import *
# from myApp.models import User
def getPageData():
    jobs = getAllJobInfo()
    jobsType = {}
    educations = ["博士","硕士","本科","大专","高中","中专/中技","学历不限"]
    workExperience = ['在校/应届生','经验不限','1-3年','3-5年','5-10年','10年以上']
    for i in jobs:
        if jobsType.get(i.type,-1) == -1:
            jobsType[i.type] = 1
        else:
            jobsType[i.type] += 1
    return educations,workExperience,jobsType.keys()

def changeSelfInfo(newInfo,FileInfo):
    user = User.objects.get(username=newInfo['username'])
    user.educational = newInfo['educational']
    user.workExpirence = newInfo['workExpirence']
    user.address = newInfo['address']
    user.work = newInfo['work']
    if FileInfo['avatar'] != None:
        user.avatar = FileInfo['avatar']
    user.save()
