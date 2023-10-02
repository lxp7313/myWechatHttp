import requests
from bs4 import BeautifulSoup
import os

from PIL import Image, ImageFilter, ImageDraw, ImageFont





# 打开图片
image = Image.open("./images/唉声叹气.png")
# 调整图像大小并税化
resized_image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS).filter(ImageFilter.SHARPEN)

# 设置空白高度
padding_top = 100

# 计算新图像的尺寸
new_width = image.width * 2
new_height = image.height * 2 + padding_top

# 创建新图像
new_image = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))

# 将原始图像粘贴到新图像中
new_image.paste(image, (0, padding_top))

# 添加文字
draw = ImageDraw.Draw(new_image)
text = "这是一行红色文字"
font = ImageFont.truetype("arial.ttf", 24)  # 字体和字号
text_width, text_height = font.getsize(text)
text_x = (new_width - text_width) // 2  # 文字水平居中
text_y = (padding_top - text_height) // 2  # 文字垂直居中
draw.text((text_x, text_y), text, font=font, fill=(255, 0, 0))  # 红色文字


# 保存处理后的图像
new_image.save("./images/sharp_唉声叹气.png")






exit(0)
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