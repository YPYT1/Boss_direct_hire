import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

# CSV文件路径
csv_file_path = 'clear.csv'

# 读取CSV文件，没有列名，所以设置header=None
df = pd.read_csv(csv_file_path, header=None)

# 检查DataFrame的列数
print(f"The CSV file has {df.shape[1]} columns.")

# 定义DataFrame的列名（确保与数据库中的列对应，不包括自增长的id列）
columns = [
    'title', 'address', 'type', 'educational', 'workExperience', 'workTag',
    'salary', 'salaryMonth', 'companyTags', 'hrWork', 'hrName', 'pratice',
    'companyTitle', 'companyAvatar', 'companyNature', 'companyStatus', 'companyPeople',
    'detailUrl', 'companyUrl', 'createTime','dist'
]

# 确保列名的数量与CSV文件中的列数匹配
if len(columns) != df.shape[1]:
    raise ValueError(f"Columns length mismatch. CSV has {df.shape[1]} columns, but {len(columns)} column names were provided.")

# 设置DataFrame的列名
df.columns = columns

# MySQL数据库连接信息
username = 'root'    # 你的MySQL用户名
password = '123456'  # 你的MySQL密码
host = 'localhost'   # 数据库服务器地址
port = 3306          # 端口号
dbname = 'boss'      # 数据库名称

# 创建数据库引擎
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}')

# 查询表中现有的记录数
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM jobinfo"))
    initial_count = result.scalar()


# 将DataFrame导入MySQL数据库，表名为jobinfo
# if_exists='replace'会替换掉原有的表，请确保这是您想要的操作
# chunksize可以根据需要设置，以便在导入大型DataFrame时分块导入
# method='multi'允许执行多行的INSERT，可以提高导入性能
df.to_sql('jobinfo', con=engine, if_exists='append', index=False, chunksize=1000, method='multi')
# 查询更新后的记录数
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM jobinfo"))
    final_count = result.scalar()
# 计算导入了多少条数据
imported_rows = final_count - initial_count
print(f'数据导入成功,{imported_rows}被导入')