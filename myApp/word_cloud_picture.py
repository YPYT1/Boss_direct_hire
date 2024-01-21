import jieba  # 分词
from matplotlib import pylab as plt     # 绘图，数据可视化
from wordcloud import WordCloud         # 词云
from PIL import Image                   # 图片处理
import numpy as np                      # 矩阵运算
from pymysql import *
import json
# wordCloud

# 所有词
def get_img(field,targetImgSrc,resImgSrc):
    con = connect(host='localhost', user='root', password='', database='boss', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select {field} from jobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i,item in enumerate(data):
        text += item[0]
    cursor.close()
    con.close()

    # 分词
    cut = jieba.cut(text)
    string = ' '.join(cut)
    print(string)

    # 图片
    img = Image.open(targetImgSrc)  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴
    # 显示生成的词语图片
    # plt.show()
    # 输入词语图片到文件
    plt.savefig(resImgSrc, dpi=500)

def get_addressCompanyTags_img(targetImgSrc,resImgSrc,addrress):
    con = connect(host='localhost', user='root', password='root', database='boss', port=3306, charset='utf8mb4')
    cursor = con.cursor()
    sql = f"select companyTags from jobinfo where address = {addrress}"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i, item in enumerate(data):
        tags = json.loads(item[0])
        for j in tags:
            text += j
    cursor.close()
    con.close()
    # 分词
    cut = jieba.cut(text)
    string = ' '.join(cut)
    print(string)
    # 图片
    img = Image.open(targetImgSrc)  # 打开遮罩图片
    img_arr = np.array(img)  # 将图片转化为列表
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)
    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 不显示坐标轴
    # 显示生成的词语图片
    # plt.show()
    # 输入词语图片到文件
    plt.savefig(resImgSrc, dpi=500)

# get_img('companyTitle',r'.\static\2.jpg',r'.\static\companyTitle.jpg')
# get_img('summary',r'.\static\2.jpg',r'.\static\summary_cloud.jpg')


