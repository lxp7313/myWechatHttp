import requests
from bs4 import BeautifulSoup
import os

# 目标网站URL
url = "http://www.hydcd.com/cy/fkccy/index4.htm"

# 发送GET请求获取网页内容
response = requests.get(url)
html_content = response.content

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html_content, "html.parser")

# 找到所有的图片标签
img_tags = soup.find_all("img")

# 遍历图片标签，并下载图片
for img in img_tags:
    # 获取图片URL
    img_url = 'http://www.hydcd.com/cy/fkccy/' + img["src"]
    print(img_url)
    # exit()

    # 获取图片标题
    img_title = img.get("alt", "")

    # 下载图片
    img_data = requests.get(img_url).content

    # 指定保存路径
    save_dir = "images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, f"{img_title}.png")

    with open(save_path, "wb") as f:
        f.write(img_data)

    print(f"已下载图片：{img_title}")