import requests
from bs4 import BeautifulSoup
import random
import os
import time
from datetime import datetime
from tqdm import tqdm
import argparse
# 搜索参数
parser = argparse.ArgumentParser(description='Process search parameters.')
parser.add_argument('-s', '--search', type=str, help='The search term or query.')
args = parser.parse_args()
s = args.search
search=s
#获取当前时间
now_time = datetime.now()
now_time_str = now_time.strftime("%Y-%m-%d-%H-%M-%S")
path2=f"./image/{now_time_str}-搜索{search}"
if not os.path.exists("/image"):
    os.mkdir("/image")
if not os.path.exists(path2):
    os.makedirs(path2)
# 文件变量名
# 参数页数
num_page=[]

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

def page_url(name,headers):
    page="https://dimtown.com/?s=%E9%9B%B7%E5%A7%86"
    r = requests.get(page, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    div_tags = soup.find_all('div', class_='nav-links')
    num_list=0
    for div in div_tags:
        nums = div.find('a', class_='page-numbers')
        print(div.get_text())

def list_images(list_url,headers):
    r2 = requests.get(list_url, headers=headers)
    r2.raise_for_status()  # 确保请求成功
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    div_tags = soup2.find_all('div', class_='cardMeta')
    image_urls = []  # 初始化一个空列表来存储图片链接
    for div in div_tags:
        # 注意：这里假设每个div中只有一个target="_blank"的a标签，且它包含图片链接
        imgs = div.find('a', target="_blank")
        if imgs and 'href' in imgs.attrs:  # 确保找到了a标签，并且它有href属性
            str_url = imgs['href']
            image_urls.append(str_url)  # 将图片链接添加到列表中

    return image_urls  # 返回包含所有图片链接的列表

def images(image_sum,headers):
        response = requests.get(image_sum,headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出异常
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div',class_='content')
        img_srcs = []
        for div in divs:
            imgs = div.find_all('img',decoding="async")
            for img in imgs:
                src = img.get('src')
                if src:  # 确保src属性存在
                    img_srcs.append(src)
                    # 返回所有提取到的src
        return img_srcs

#程序开始检测页数
page_nums=range(1,11)
now_pages=0
now_urls=[]
print("爬虫开始运行....")
print("开始检测页数.....")
for page_num in page_nums:
    r3 = requests.get(f"https://dimtown.com/page/{page_num}?s={search}",headers=headers)
    if r3.url != "https://dimtown.com/":
        now_pages+=1
        print(r3.url)
        now_urls.append(r3.url)
    else:
        break
print(f"检测成功一共有 {now_pages} 页")
print("即将爬取全部内......")
# 爬取数据
for now_url in now_urls:
    print(now_url)
    date_list = list_images(now_url,headers)
    for date in date_list:
        print(date)
        down_images= images(date,headers)
        for down_image in down_images:
          try:
            s_name = down_image[-4:]
            random_int = random.randint(10000, 9999999)
            file_name = f"image/{now_time_str}-搜索{search}/{now_time_str}{random_int}{s_name}"
            r4 = requests.get(down_image, headers=headers)
            if r4.status_code==200:
                print(f"关键词:{search}:'{down_image}' :successful!")
                with open(file_name, 'wb') as f:
                    f.write(r4.content)
            else:
                print("error 图片已失效")
          except Exception as e:
              print(e)


for i in tqdm(range(500)):
    time.sleep(0.01)

print("已经全部加载完成")
