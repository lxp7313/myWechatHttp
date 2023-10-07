import schedule
import time
import threading
from fastapi import Body, FastAPI, Request, Response
import uvicorn
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import requests
import os
import random
from func_chengyu import Chengyu

app = FastAPI()
chengyu = Chengyu()

class Msg(BaseModel):
    id: int
    ts: int
    sign: str
    type: int
    xml: str
    sender: str
    roomid: str
    content: str
    thumb: str
    extra: str
    is_at: bool
    is_self: bool
    is_group: bool

class wx_http():
    def __init__(self) -> None:
        self.conn = sqlite3.connect('wx_contact.db')
        self.chengyu = ''

    async def msg_cb(self, Msg = Body(description="微信消息"), response= Response):
        print(f"收到消息：{Msg}")
        # self.updateContact(Msg)
        self.processMsg(Msg)

        return {"status": 500, "message": "成功"}
    def processMsg(self, Msg):
        wxid = Msg['sender']
        roomid = Msg['roomid']
        content = Msg['content']
        is_at = Msg['is_at']
        print(f"{wxid}[{roomid}]:{content}")
        if(roomid != ''):
            cb = 'http://localhost:9999/alias-in-chatroom/'
            params = {
                "roomid": roomid,
                "wxid": wxid,
            }
            rsp = requests.get(url=cb, params=params, timeout=30)
            group_alias_cark = rsp.json()
            group_nickname = group_alias_cark['data']['alias']

            conn = sqlite3.connect('wx_contact.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Contacts WHERE wxid=?", (roomid,))
            room_rs = cursor.fetchone()
            print(f"room_rs:{room_rs}")
            if(room_rs['chengyu_open'] == 1 and room_rs['chengyu'] != '' and content == room_rs['chengyu']):
                chengyu_mean = chengyu.getMeaning(content)
                print(chengyu_mean)

                cb = 'http://localhost:9999/text'
                data = {
                    "msg": "@" + group_nickname + " \n恭喜你，答对了\n" + chengyu_mean,
                    "receiver": roomid,
                    "aters": wxid,
                }
                rsp = requests.post(url=cb, json=data, timeout=30)
                self.chengyu = ''
                print(rsp)

                cursor.execute("UPDATE Contacts SET chengyu = '' where wxid = '" + roomid + "'")
                conn.commit()
            elif(is_at == True):
                from func_chatgpt import ChatGPT
                chargpt = {
                    'key': 'sk-BZh0SXyYQ6XSi6KG81533eBd148449B794395fC6349559A1',
                    'api': 'https://api.catgpt.im/v1',  # https://api.openai.com/v1
                    # 'api': 'https://api.catgpt.im/v1',# https://api.openai.com/v1
                    'proxy': '',  # http://127.0.0.1:21882
                    'prompt': 'gpt3.5'
                }
                chat = ChatGPT(chargpt["key"], chargpt["api"], chargpt["proxy"], chargpt["prompt"])

                q = content
                rsp = chat.get_answer(q, wxid)
                print(rsp)

                cb = 'http://localhost:9999/text'
                data = {
                    "msg": "@" + group_nickname + " " + rsp,
                    "receiver": roomid,
                    "aters": wxid,
                }
                rsp = requests.post(url=cb, json=data, timeout=30)
                self.chengyu = ''
                print(rsp)
            conn.close()
        elif(wxid == 'wxid_mboc06esypzm19'):
            cb = 'http://localhost:9999/text'
            data = {
                "msg":"你吃饭了没",
                 "receiver":wxid
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            print(rsp)

    def updateContact(self, Msg):
        wxid = Msg['sender']
        roomid = Msg['roomid']
        content = Msg['content']
        print(f"{wxid}[{roomid}]:{content}")

        conn = sqlite3.connect('wx_contact.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Contacts WHERE wxid=?", (wxid,))
        existing_user = cursor.fetchone()
        # print(existing_user)
        if existing_user == None:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO Contacts (wxid, code, remark, name, country, province, city, gender, addTime, editTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (wxid, '', '', '', '', '', '', '', formatted_time, formatted_time))
            conn.commit()

        if roomid != '':
            cursor.execute("SELECT * FROM Contacts WHERE wxid=?", (roomid,))
            existing_room = cursor.fetchone()
            if existing_room == None:
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO Contacts (wxid, code, remark, name, country, province, city, gender, addTime, editTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (roomid, '', '', '', '', '', '', '', formatted_time, formatted_time))
                conn.commit()

        conn.close()
    def chengyu_send(self):
        print("定时任务执行中...")
        # 指定图片所在的文件夹路径
        img_folder = "./images"
        # 获取文件夹中所有的图片文件路径
        img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if
                     f.endswith(".jpg") or f.endswith(".png")]

        conn = sqlite3.connect('wx_contact.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Contacts WHERE chengyu_open=1")
        contacts_array = cursor.fetchall()
        for r in contacts_array:
            # 随机选择一个图片文件路径
            rand_img_file = random.choice(img_files)

            current_dir = os.getcwd()
            print(current_dir)
            print(rand_img_file)
            self.chengyu = chengyu = rand_img_file.split('\\')[1].split('.')[0]
            print(chengyu)
            file_img = current_dir + rand_img_file[1:].replace('/', '\\')
            print(file_img)

            cursor.execute("UPDATE Contacts SET chengyu = '" + chengyu + "' where wxid = '" + r['wxid'] + "'")
            conn.commit()

            cb = 'http://localhost:9999/image'
            data = {
                "path": file_img,
                "receiver": r['wxid'],#wxid_mboc06esypzm19[34502871363@chatroom]
                "aters":"",
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            print(rsp)

            cb = 'http://localhost:9999/text'
            data = {
                "msg": chengyu,
                 "receiver": "filehelper"
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            print(rsp)
    def weather_send(self):
        conn = sqlite3.connect('wx_contact.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Contacts WHERE weather_code<>''")
        contacts_array = cursor.fetchall()
        for r in contacts_array:
            url = 'https://devapi.qweather.com/v7/weather/3d?location='+ r['weather_code'] +'&key=a7a8020835354483ac47da08f3287164'
            response = requests.get(url)
            contents = response.json()
            # print(contents)
            data = contents['daily']
            print(data)
            text = r['weather'] +'今日天气：'
            text += data[0]['textDay']
            if (data[0]['textNight'] != data[0]['textDay']):
                text += '转' + data[0]['textNight']
            text += '，温度：' + data[0]['tempMin']
            text += '°C~' + data[0]['tempMax'] + '°C'
            text += '，' + data[0]['windDirDay'] + data[0]['windScaleDay'] + '级'
            text += '。日出时间：' + data[0]['sunrise']
            text += '，日落时间：' + data[0]['sunset'] + '。'
            text += "\n" + contents['fxLink']
            print(text)

            cb = 'http://localhost:9999/text'
            data = {
                "msg": text,
                "receiver": r['wxid'],#wxid_mboc06esypzm19[34502871363@chatroom]
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            print(rsp)

wx_http = wx_http()
def main():
    app.add_api_route("/msg_cb", wx_http.msg_cb, methods=["POST"], summary="接收消息回调样例", tags=["示例"])

    uvicorn.run(app, host="localhost", port=10000)

# 定义任务函数
# def task():
#     print("定时任务执行中...")
#     # 指定图片所在的文件夹路径
#     img_folder = "./images"
#     # 获取文件夹中所有的图片文件路径
#     img_files = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if
#                  f.endswith(".jpg") or f.endswith(".png")]
#
#     # 随机选择一个图片文件路径
#     rand_img_file = random.choice(img_files)
#
#     current_dir = os.getcwd()
#     print(current_dir)
#     print(rand_img_file)
#     file_img = current_dir + rand_img_file[1:].replace('/','\\')
#     print(file_img)
#
#     cb = 'http://localhost:9999/image'
#     data = {
#         "path": file_img,
#         "receiver": "wxid_cf5vewq4pwzj21"
#     }
#     rsp = requests.post(url=cb, json=data, timeout=30)
#     print(rsp)


if __name__ == '__main__':
    #wx_http.weather_send()
    #exit(0)
    #wx_http.chengyu_send()

    #main()
    # exit(0)

    # 创建定时任务线程
    schedule_thread = threading.Thread(target=main, args=())
    schedule_thread.start()

    # 创建定时任务线程
    schedule_thread1 = threading.Thread(target=schedule.every().day.at("17:30").do, args=(wx_http.chengyu_send,))
    schedule_thread1.start()

    # 创建定时任务线程
    schedule_thread2 = threading.Thread(target=schedule.every().day.at("07:00").do, args=(wx_http.weather_send,))
    schedule_thread2.start()


    while True:
        schedule.run_pending()
        time.sleep(1)