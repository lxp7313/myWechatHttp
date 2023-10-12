from pathlib import Path

import requests
from bs4 import BeautifulSoup
import os

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import json
import urllib3

from func_chatgpt import ChatGPT
from datetime import datetime




# 格式化为字符串并打印
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
print(formatted_time)

cb = 'http://localhost:9999/pyq/'
params = {
    "id": '0',
}
# 收到消息：{'id': 9031054296394415394, 'ts': 1697096244, 'sign': '7959c1f6800978e0823c7a73d538d4ed', 'type': 47, 'xml': '<msgsource>\n\t<silence>1</silence>\n\t<membercount>13</membercount>\n\t<signature>v1_3k03ZCRy</signature>\n\t<tmp_node>\n\t\t<publisher-id></publisher-id>\n\t</tmp_node>\n</msgsource>\n', 'sender': 'YiQ108', 'roomid': '7700923334@chatroom', 'content': '<msg><emoji fromusername = "YiQ108" tousername = "7700923334@chatroom" type="2" idbuffer="media:0_0" md5="4b250df240eb4da0a0402b8b5cd64a89" len = "211729" productid="" androidmd5="4b250df240eb4da0a0402b8b5cd64a89" androidlen="211729" s60v3md5 = "4b250df240eb4da0a0402b8b5cd64a89" s60v3len="211729" s60v5md5 = "4b250df240eb4da0a0402b8b5cd64a89" s60v5len="211729" cdnurl = "http://wxapp.tc.qq.com/262/20304/stodownload?m=4b250df240eb4da0a0402b8b5cd64a89&amp;filekey=30350201010421301f020201060402534804104b250df240eb4da0a0402b8b5cd64a890203033b11040d00000004627466730000000132&amp;hy=SH&amp;storeid=2630e14bc00030d3b000000000000010600004f50534808367b40b7c6573de&amp;bizid=1023" designerid = "" thumburl = "" encrypturl = "http://wxapp.tc.qq.com/262/20304/stodownload?m=9a0098104f3550ac578eac481015f6bb&amp;filekey=30350201010421301f020201060402534804109a0098104f3550ac578eac481015f6bb0203033b20040d00000004627466730000000132&amp;hy=SH&amp;storeid=2630e14bc00073bd5000000000000010600004f5053480d167b40b7ca4efdc&amp;bizid=1023" aeskey= "4ba755354537be951b34b9471f277875" externurl = "http://wxapp.tc.qq.com/262/20304/stodownload?m=c2f04a00a91b681402099c010bf07131&amp;filekey=30340201010420301e02020106040253480410c2f04a00a91b681402099c010bf0713102026700040d00000004627466730000000132&amp;hy=SH&amp;storeid=2630e14bc000a15ec000000000000010600004f50534819c65b40b7c6d2acc&amp;bizid=1023" externmd5 = "9fccb2614ba4e088f0707e6339077588" width= "300" height= "300" tpurl= "" tpauthkey= "" attachedtext= "" attachedtextcolor= "" lensid= "" emojiattr= "" linkid= "" desc= "" ></emoji> <gameext type="0" content="0" ></gameext></msg>', 'thumb': '', 'extra': '', 'is_at': False, 'is_self': False, 'is_group': True}

rsp = requests.get(url=cb, params=params, timeout=30)
# group_alias_cark = rsp.text
# group_nickname = group_alias_cark['data']['alias']
print(rsp)

# 格式化为字符串并打印
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
print(formatted_time)

exit(0)


# url = 'https://devapi.qweather.com/v7/weather/3d?location=101210103&key=a7a8020835354483ac47da08f3287164'
# response = requests.get(url)
# data = response.json()
# data = data['daily']
# print(data)
# text = '桐庐今日天气：'
# text += data[0]['textDay']
# if(data[0]['textNight'] != data[0]['textDay']):
#     text += data[0]['textNight']
# text += '，温度：' + data[0]['tempMin']
# text += '°C~' + data[0]['tempMax'] + '°C'
# text += '，' + data[0]['windDirDay'] + data[0]['windScaleDay'] + '级'
# text += '。日出时间：' + data[0]['sunrise']
# text += '，日落时间：' + data[0]['sunset'] + '。'
# print(text)
# exit(0)

# 获取当前时间

# 格式化为字符串并打印
# current_time = datetime.now()
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
# print(formatted_time)
#
# # chatgpt
# chargpt = {
#     'key': 'Link_kRFp6JccNVvHXuWSNFM9uhtxNKeKcdsxK4yKtlL0gn-tNb5Vm57',
#     'api': 'https://api.link-ai.chat/v1',
#     # 'key': 'sk-BZh0SXyYQ6XSi6KG81533eBd148449B794395fC6349559A1',
#     # 'api': 'https://api.catgpt.im/v1',
#     # 'key': 'sk-ywvVhPvlXWNXhaSW9a5c310bD94f44F7BdE028Cb58470dF5',
#     # 'api': 'https://api.chat8.tech/v1',# https://api.openai.com/v1
#     # 'key': 'sk-376bkdfy8FiC3Pyg108bF1A62b8e4b9aA85fE30eAd7635Eb',
#     # 'api': 'https://api.foforise.xyz/v1',
#     'proxy': '', #http://127.0.0.1:21882
#     'prompt': 'gpt-3.5-turbo-16k'
# }
# chat = ChatGPT(chargpt["key"], chargpt["api"], chargpt["proxy"], chargpt["prompt"])
#
# q = '阿糖好看吗'
# rsp = chat.get_answer(q, "wxid")
# print(rsp)
#
# # 获取当前时间
# current_time = datetime.now()

# 格式化为字符串并打印
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
# print(formatted_time)
#
# exit(0)


#
# # chatgpt
# chargpt = {
#     # 'api': 'https://api.openai.com/v1',
#     # 'key': 'sk-BZh0SXyYQ6XSi6KG81533eBd148449B794395fC6349559A1',
#     # 'api': 'https://api.catgpt.im/v1',
#     'key': 'sk-376bkdfy8FiC3Pyg108bF1A62b8e4b9aA85fE30eAd7635Eb',
#     'api': 'https://api.foforise.xyz/v1/chat/completions',
#     'proxy': '', #http://127.0.0.1:21882
#     'prompt': 'gpt3.5'
# }
# # chatgpt:
# #   key: 填写你 ChatGPT 的 key
# #   api: https://api.openai.com/v1 # 如果你不知道这是干嘛的，就不要改
# #   proxy: # 如果你在国内，你可能需要魔法，大概长这样：http://域名或者IP地址:端口号
# #   prompt: 你是智能聊天机器人，你叫wcferry # 根据需要对角色进行设定
# chat = ChatGPT(chargpt["key"], chargpt["api"], chargpt["proxy"], chargpt["prompt"])
#
# q = '2*2等于几'
# rsp = chat.get_answer(q, "wxid")
# print(rsp)
#
# q = '再加3等于几'
# rsp = chat.get_answer(q, "wxid")
# print(rsp)
# exit(0)




# 禁用证书验证警告
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
# # 测试
#
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer sk-376bkdfy8FiC3Pyg108bF1A62b8e4b9aA85fE30eAd7635Eb',
# }
#
# data = {
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "你是谁"}]
# }
# json_data = json.dumps(data)
#
# response = requests.post('https://api.foforise.xyz/v1/chat/completions', headers=headers, data=json_data, verify=False)
# print(response)
# data = response.json()
# print(data)
# exit(0)




# 文件夹内的图片，放大一倍加锐化
img_folder = "./images"
# 获取文件夹中所有的图片文件路径
img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if
             f.endswith(".jpg") or f.endswith(".png")]
for i in img_files:
    print(i)
    file_img = i.split('\\')[1]
    print(file_img)
    # 打开图片
    image = Image.open(i)
    # 调整图像大小并税化
    resized_image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS).filter(ImageFilter.SHARPEN)

    # 设置空白高度
    padding_top = 50

    # 计算新图像的尺寸
    new_width = image.width * 2
    new_height = image.height * 2 + padding_top

    # 创建新图像
    new_image = Image.new("RGBA", (new_width, new_height), color=(255, 255, 255, 0))

    # 将原始图像粘贴到新图像中
    new_image.paste(resized_image, (0, padding_top))

    # 添加文字
    draw = ImageDraw.Draw(new_image)
    text = "看图猜成语"
    font = ImageFont.truetype("STXINWEI.TTF", 24)  # 字体和字号
    text_width, text_height = draw.textsize(text, font)
    text_x = (new_width - text_width) // 2  # 文字水平居中
    text_y = (padding_top - text_height) // 2  # 文字垂直居中
    draw.text((text_x, text_y), text, font=font, fill=(255, 0, 0))  # 红色文字


    # 保存处理后的图像
    new_image.save("./images/new/" + file_img)






exit(0)

# 获取目标网站图片
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