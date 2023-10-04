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
        self.updateContact(Msg)
        self.processMsg(Msg)

        return {"status": 500, "message": "成功"}
    def processMsg(self, Msg):
        wxid = Msg['sender']
        roomid = Msg['roomid']
        content = Msg['content']
        print(f"{wxid}[{roomid}]:{content}")
        if(self.chengyu != '' and self.chengyu == content):
            chengyu = Chengyu()
            chengyu_mean = chengyu.getMeaning(self.chengyu)
            print(chengyu_mean)

            cb = 'http://localhost:9999/text'
            data = {
                "msg":"恭喜你，答对了\n" + chengyu_mean,
                 "receiver":"filehelper"
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            self.chengyu = ''
            print(rsp)

        elif(wxid == 'wxid_mboc06esypzm19'):
            cb = 'http://localhost:9999/text'
            data = {
                "msg":"你吃饭了没",
                 "receiver":"wxid_mboc06esypzm19"
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            print(rsp)

    def updateContact(self, Msg):
        wxid = Msg['sender']
        roomid = Msg['roomid']
        content = Msg['content']
        print(f"{wxid}[{roomid}]:{content}")

        conn = sqlite3.connect('wx_contact.db')
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

        # 随机选择一个图片文件路径
        rand_img_file = random.choice(img_files)

        current_dir = os.getcwd()
        print(current_dir)
        print(rand_img_file)
        self.chengyu = chengyu = rand_img_file.split('\\')[1].split('.')[0]
        print(chengyu)
        file_img = current_dir + rand_img_file[1:].replace('/', '\\')
        print(file_img)

        cb = 'http://localhost:9999/image'
        data = {
            "path": file_img,
            "receiver": "filehelper"
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
    wx_http.chengyu_send()
    #exit(0)

    # 创建定时任务线程
    #schedule_thread = threading.Thread(target=schedule.every().day.at("17:29").do, args=(wx_http.chengyu_send,))
    #schedule_thread.start()

    # 创建定时任务线程
    schedule_thread1 = threading.Thread(target=main, args=())
    schedule_thread1.start()


    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()