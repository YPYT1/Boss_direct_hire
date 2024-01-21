from myApp.models import JobInfo
import pandas as pd
from .publicData import *

timesalary = pd.read_csv("data.txt")
import matplotlib.pyplot as plt
import matplotlib.pylab as pyl
def getmodelspre():
    jobsInfos = JobInfo.objects.exclude(workExperience ='经验不限')
    listtime=jobsInfos.objects.values_list('workExperience', flat=True)
    listsalary=jobsInfos.objects.values_list('salary', flat=True)
    list1=[]
    for l in listtime:
        if len(l)==3:
            worktime=int(l[0])/12
        elif len(l)==4:
            if l[1]=='-':
                worktime=int(l[2])
            elif l[1]=='年':
                worktime=int(l[0])
        elif len(l)==5:
            if l[2]=='/':
                worktime=0
            else:
                worktime=int(l[:2])
        list1.append(worktime)
    print(list1)

    list2=[]
    for salary in listsalary:
        salaryres=(salary[0]+salary[1])/2
        list2.append(salaryres)
    print(list2)

    with open('filename.txt', 'w') as f:
        f.write('均资元,工时年\n')
        for i in range(len(list1)):
            f.write(str(list2[i]) + ",")
            f.write(str(list1[i]) + "\n")
    f.close()

    plt.rcParams['font.sans-serif'] = ['SimHei']
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    feature_cols = ['工时年']
    X = timesalary[feature_cols]
    y = timesalary.均资元
    model.fit(X,y)
    plt.scatter(timesalary.工时年, timesalary.均资元)
    plt.plot(timesalary.工时年, model.predict(X) , color='blue')
    pyl.title("y="+str(model.coef_[0])+"x+"+str(model.intercept_))
    plt.xlabel('工时年')
    plt.ylabel('均资元')
    plt.savefig('yuce.png')
    plt.show()
    print("截距与斜率:",model.intercept_,model.coef_)
    print("该线性回归方程组公式为：y="+str(model.coef_[0])+"x+"+str(model.intercept_))