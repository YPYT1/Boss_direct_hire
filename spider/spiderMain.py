import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import pandas as pd
import os
import django
from datetime import datetime
from selenium.webdriver.chrome.service import Service
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss直聘数据可视化分析.settings')
django.setup()
from myApp.models import *
class spider(object):
    def __init__(self,type,page):
        self.type = type
        self.page = page
        self.spiderUrl = "https://www.zhipin.com/web/geek/job?query=%s&city=100010000&page=%s"

    def startBrower(self):
        s = Service("chromedriver.exe")
        browser = webdriver.Chrome(service=s)
        # browser=webdriver.Chrome(executable_path='./chromedriver.exe')
        return browser

    def main(self,**info):
        if info['page'] < self.page:return
        brower = self.startBrower()
        print('页表页面URL:' + self.spiderUrl % (self.type,self.page))
        brower.get(self.spiderUrl % (self.type,self.page))
        time.sleep(15)
        # return
        # //*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[1]/ul
        job_list = brower.find_elements(by=By.XPATH, value="//ul[@class='job-list-box']/li")
        for index,job in enumerate(job_list):
            try:
                print("爬取的是第 %d 条" % (index + 1))
                jobData = []
                # title  工作名字
                title = job.find_element(by=By.XPATH,
                                         value=".//div[contains(@class,'job-title')]/span[@class='job-name']").text
                # address  地址
                addresses = job.find_element(by=By.XPATH,
                                           value=".//div[contains(@class,'job-title')]//span[@class='job-area']").text.split(
                    '·')
                address = addresses[0]
                # dist 行政区
                if len(addresses) != 1:dist = addresses[1]
                else: dist = ''
                # type  工作类型
                type = self.type
               # // *[ @ id = "wrap"] / div[2] / div[2] / div / div[1] / div[1] / ul / li[5] / div[1] / div / div[2] / ul
                tag_list = job.find_elements(by=By.XPATH,
                                             value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li")
                if len(tag_list) == 2:
                    educational = job.find_element(by=By.XPATH,
                                                   value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[2]").text
                    workExperience = job.find_element(by=By.XPATH,
                                                      value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[1]").text
                else:
                    educational = job.find_element(by=By.XPATH,
                                                   value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[3]").text
                    workExperience = job.find_element(by=By.XPATH,
                                                      value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[2]").text
                # hr
                hrWork = job.find_element(by=By.XPATH,
                                          value=".//div[contains(@class,'job-info')]/div[@class='info-public']/em").text
                hrName = job.find_element(by=By.XPATH,
                                          value=".//div[contains(@class,'job-info')]/div[@class='info-public']").text

                # workTag 工作标签
                workTag = job.find_elements(by=By.XPATH,
                                            value="./div[contains(@class,'job-card-footer')]/ul[@class='tag-list']/li")
                workTag = json.dumps(list(map(lambda x: x.text, workTag)))

                # salary 薪资
                salaries = job.find_element(by=By.XPATH,
                                            value=".//div[contains(@class,'job-info')]/span[@class='salary']").text
                # 是否为实习单位
                pratice = 0
                if salaries.find('K') != -1:
                    salaries = salaries.split('·')
                    if len(salaries) == 1:
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = '0薪'
                    else:
                        # salaryMonth 年底多薪
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = salaries[1]
                else:
                    salary = list(map(lambda x: int(x), salaries.replace('元/天', '').split('-')))
                    salaryMonth = '0薪'
                    pratice = 1

                # companyTitle 公司名称
                companyTitle = job.find_element(by=By.XPATH, value=".//h3[@class='company-name']/a").text
                # companyAvatar 公司头像
                companyAvatar = job.find_element(by=By.XPATH,
                                                 value=".//div[contains(@class,'job-card-right')]//img").get_attribute(
                    "src")
                companyInfoList = job.find_elements(by=By.XPATH,
                                                    value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li")
                if len(companyInfoList) == 3:
                    companyNature = job.find_element(by=By.XPATH,
                                                     value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[1]").text
                    companyStatus = job.find_element(by=By.XPATH,
                                                     value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[2]").text
                    try:
                        companyPeople = list(map(lambda x: int(x), job.find_element(by=By.XPATH,
                                                                                    value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[3]").text.replace(
                            '人', '').split('-')))
                    except:
                        companyPeople = [0, 10000]
                else:
                    companyNature = job.find_element(by=By.XPATH,
                                                     value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[1]").text
                    companyStatus = "未融资"
                    try:
                        companyPeople = list(map(lambda x: int(x), job.find_element(by=By.XPATH,
                                                                                    value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[2]").text.replace(
                            '人', '').split('-')))
                    except:
                        companyPeople = [0, 10000]
                # companyTag 公司标签
                companyTag = job.find_element(by=By.XPATH,
                                              value="./div[contains(@class,'job-card-footer')]/div[@class='info-desc']").text
                if companyTag:
                    companyTag = json.dumps(companyTag.split('，'))

                else:
                    companyTag = '无'

                # 详情地址
                detailUrl = job.find_element(by=By.XPATH,
                                             value="./div[@class='job-card-body clearfix']/a").get_attribute('href')
                # 公司详情
                companyUrl = job.find_element(by=By.XPATH, value="//h3[@class='company-name']/a").get_attribute('href')

                createTime = datetime.now().strftime('%Y-%m-%d')

                jobData.append(title)
                jobData.append(address)
                jobData.append(type)
                jobData.append(educational)
                jobData.append(workExperience)
                jobData.append(workTag)
                jobData.append(salary)
                jobData.append(salaryMonth)
                jobData.append(companyTag)
                jobData.append(hrWork)
                jobData.append(hrName)
                jobData.append(pratice)
                jobData.append(companyTitle)
                jobData.append(companyAvatar)
                jobData.append(companyNature)
                jobData.append(companyStatus)
                jobData.append(companyPeople)
                jobData.append(detailUrl)
                jobData.append(companyUrl)
                jobData.append(createTime)
                jobData.append(dist)
                self.save_to_csv(jobData)
            except:
                pass

        self.page += 1
        self.main(page=info['page'])

    def save_to_csv(self,rowData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)

    def clear_numTemp(self):
        with open('./numTemp.txt','w',encoding='utf-8') as f:
            f.write('')

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv','a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["title","address","type","educational","workExperience","workTag","salary","salaryMonth",
                                 "companyTags","hrWork","hrName","pratice","companyTitle","companyAvatar","companyNature",
                                 "companyStatus","companyPeople","detailUrl","companyUrl","createTime","dist"])

    def save_to_sql(self):
        data = self.clearData()
        for job in data:
            JobInfo.objects.create(
                title=job[0],
                address = job[1],
                type = job[2],
                educational = job[3],
                workExperience = job[4],
                workTag = job[5],
                salary = job[6],
                salaryMonth = job[7],
                companyTags = job[8],
                hrWork = job[9],
                hrName = job[10],
                pratice = job[11],
                companyTitle = job[12],
                companyAvatar = job[13],
                companyNature = job[14],
                companyStatus = job[15],
                companyPeople = job[16],
                detailUrl = job[17],
                companyUrl = job[18],
                createTime= job[19],
                dist=job[20]
            )
        print("导入数据库成功")
        # 如果不想保留文件
        #os.remove("./temp.csv")

    # def clearData(self):
    #     df = pd.read_csv('./temp.csv')
    #     df.dropna(inplace=True)
    #     df.drop_duplicates(inplace=True)
    #     df['salaryMonth'] = df['salaryMonth'].map(lambda x:x.replace('薪',''))
    #     print("总条数为%d" %  df.shape[0])
    #     return df.values
    def clearData(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        # 检查 DataFrame 中是否存在 'salaryMonth' 列
        if 'salaryMonth' in df.columns:
            df['salaryMonth'] = df['salaryMonth'].map(lambda x: x.replace('薪', ''))

        print("总条数为%d" % df.shape[0])
        return df.values


if __name__ == '__main__':
    spiderObj = spider("大数据",14)
    spiderObj.init()
    spiderObj.main(page=16)
    spiderObj.save_to_sql()