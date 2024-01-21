# 这是一个基于BOSS直聘实现的数据爬取与可视化分析
运行代码前要先导入数据库，先自行创建一个数据库，名叫boss；\
在运行boss.sql文件在boss数据库中创建数据表\
运行项目前要在setting.py中配置数据库连接
>DATABASES = {
    'default':{
      'ENGINE':'django.db.backends.mysql',
      'NAME':'boss',
      'USER':'数据库账户名',
      'PASSWORD':'数据库密码',
      'HOST':"localhost",
      'PORT':'3306'
    }
  }\

在spider目录中，spiderMain.py是爬虫文件，如果你要保留爬取到的数据文件，只需注释掉**os.remove("./temp.csv")**，
## 页面效果展示
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/3c24eb1f-29d6-4606-a639-75f1884757ff)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/2831dbdd-0ee3-4e73-90ce-53cfaea74e94)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/f3ceecb8-0a47-4a54-b1a4-b21b9c03d63e)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/610cb19a-28a2-4512-b1af-50b27c726f82)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/0bf4878a-d3a0-449d-b921-df8376761bd4)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/434b33d5-d785-43e5-b2c2-0852a1aed812)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/ce6b3feb-fcaf-4751-8287-56f00d452eda)\
![image](https://github.com/YPYT1/Boss_direct_hire/assets/95224342/ec7ce08c-b900-43e0-99fa-33e3f80213e6)\





