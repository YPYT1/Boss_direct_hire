from myApp.models import User,JobInfo

educations = {"博士": 1, "硕士": 2, "本科": 3, "大专": 4, "高中": 5, "中专/中技": 6, "初中及以下":7,"学历不限": 8,"无": 9}
workExpirences = ['在校/应届','经验不限','1年以内','1-3年','3-5年','5-10年','10年以上']
companyPeople = ['20人以下','100人以下','500人以下','1000人以下','1万人以下','1万人以上']
salaryList = ['0-10k', '10-20k', '20-30k', '30-40k', '40k以上']

def getAllUser():
    return User.objects.all()

def getAllJobInfo():
    jobsInfos = JobInfo.objects.all()
    return jobsInfos

def getTypes():
    jobsInfos = JobInfo.objects.all()
    typesList = []
    for i in jobsInfos:typesList.append(i.type)
    return list(set(typesList))

def getAddress():
    jobsInfos = JobInfo.objects.all()
    addressList = []
    for i in jobsInfos: addressList.append(i.address)
    return list(set(addressList))