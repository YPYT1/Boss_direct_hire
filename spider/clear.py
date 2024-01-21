import pandas as pd

# 读取temp.csv文件
temp_df = pd.read_csv('temp.csv', header=None)

# 判断temp_df是否为空
if temp_df.empty:
    print("temp.csv 文件为空，停止工作。")
else:
    # 判断clear.csv文件是否存在
    try:
        clear_df = pd.read_csv('clear.csv', header=None)
    except pd.errors.EmptyDataError:
        clear_df = pd.DataFrame()

    # 判断clear_df是否为空
    if clear_df.empty:
        # 对temp.csv的数据进行清洗和填补缺失值
        temp_df.fillna('无', inplace=True)

        # 更新clear.csv文件
        temp_df.to_csv('clear.csv', header=False, index=False)
        print("clear.csv 文件为空，已写入清洗和填补缺失值后的 temp.csv 中的数据。")
    else:
        # 删除clear.csv中和temp.csv相同的行
        merged_df = pd.concat([temp_df, clear_df]).drop_duplicates(keep=False)

        # 使用 "无" 替换空值
        merged_df.fillna('无', inplace=True)

        # 更新clear.csv文件
        merged_df.to_csv('clear.csv', header=False, index=False)
        print("清洗完成，并更新 clear.csv 文件。")
