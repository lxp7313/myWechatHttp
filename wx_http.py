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
import re
from func_chengyu import Chengyu
from func_weather import Weather

app = FastAPI()
cy = Chengyu()

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

        # 格式化为字符串并打印
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        print('回调时间：' + formatted_time)

        self.updateContact(Msg)

        # 格式化为字符串并打印
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        print('更新联系人时间：' + formatted_time)

        if(Msg['type'] == 1):
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

            content = content.replace("@" + group_nickname + ' ', '')
            content = content.replace("@" + group_nickname, '')

            # 格式化为字符串并打印
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            print('获取群昵称时间：' + formatted_time)

            conn = sqlite3.connect('wx_contact.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Contacts WHERE wxid=?", (roomid,))
            room_rs = cursor.fetchone()
            print(f"room_rs:{room_rs}")

            # 格式化为字符串并打印
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            print('获取房间信息时间：' + formatted_time)

            if(room_rs['chengyu_open'] == 1 and room_rs['chengyu'] != '' and content == room_rs['chengyu']):
                chengyu_mean = cy.getMeaning(content)
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
            elif(content[-2:] == '天气'):
                times = re.findall(r"(今天|明天|后天|今日|明日|后日)", content)
                day = 0
                print(times)
                if len(times) > 0:
                    times = times[0]
                    if (times == '今天' or times == '今日'):
                        day = 0
                    elif (times == '明天' or times == '明日'):
                        day = 1
                    elif (times == '后天' or times == '后日'):
                        day = 2
                content = re.sub(r"[^\u4e00-\u9fa5]", "", content)
                content = re.sub(r"今天|明天|后天|今日|明日|后日|天气", "", content)

                wt = Weather()
                text = wt.get_text(content, day)

                cb = 'http://localhost:9999/text'
                data = {
                    "msg": text,
                    "receiver": roomid,  # wxid_mboc06esypzm19[34502871363@chatroom]
                }
                rsp = requests.post(url=cb, json=data, timeout=30)
                print(rsp)
            elif(content == '猜谜' or content == '猜谜语' or content == '猜成语' or content == '看图猜成语'):
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

                cursor.execute("UPDATE Contacts SET chengyu = '" + chengyu + "' where wxid = '" + roomid + "'")
                conn.commit()

                cb = 'http://localhost:9999/image'
                data = {
                    "path": file_img,
                    "receiver": roomid,  # wxid_mboc06esypzm19[34502871363@chatroom]
                    "aters": "",
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
            elif(is_at == True):
                from func_chatgpt import ChatGPT
                chargpt = {
                    'key': 'Link_kRFp6JccNVvHXuWSNFM9uhtxNKeKcdsxK4yKtlL0gn-tNb5Vm57',
                    'api': 'https://api.link-ai.chat/v1',
                    # 'key': 'sk-BZh0SXyYQ6XSi6KG81533eBd148449B794395fC6349559A1',
                    # 'api': 'https://api.catgpt.im/v1',
                    # 'key': 'sk-ywvVhPvlXWNXhaSW9a5c310bD94f44F7BdE028Cb58470dF5',
                    # 'api': 'https://api.chat8.tech/v1',# https://api.openai.com/v1
                    # 'key': 'sk-376bkdfy8FiC3Pyg108bF1A62b8e4b9aA85fE30eAd7635Eb',
                    # 'api': 'https://api.foforise.xyz/v1',
                    'proxy': '',  # http://127.0.0.1:21882
                    'prompt': 'gpt-3.5-turbo-16k'
                }
                chat = ChatGPT(chargpt["key"], chargpt["api"], chargpt["proxy"], chargpt["prompt"])

                q = content
                rsp = chat.get_answer(q, wxid)
                print(rsp)

                # 格式化为字符串并打印
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                print('获取GPT答案时间：' + formatted_time)

                cb = 'http://localhost:9999/text'
                data = {
                    "msg": "@" + group_nickname + " " + rsp,
                    "receiver": roomid,
                    "aters": wxid,
                }
                rsp = requests.post(url=cb, json=data, timeout=30)
                self.chengyu = ''
                print(rsp)

                # 格式化为字符串并打印
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                print('发送完成时间：' + formatted_time)
            conn.close()
        elif(wxid == 'wxid_mboc06esypzm19' or wxid == 'wxid_cf5vewq4pwzj21'):
            from func_chatgpt import ChatGPT
            chargpt = {
                'key': 'Link_kRFp6JccNVvHXuWSNFM9uhtxNKeKcdsxK4yKtlL0gn-tNb5Vm57',
                'api': 'https://api.link-ai.chat/v1',
                # 'key': 'sk-BZh0SXyYQ6XSi6KG81533eBd148449B794395fC6349559A1',
                # 'api': 'https://api.catgpt.im/v1',
                # 'key': 'sk-ywvVhPvlXWNXhaSW9a5c310bD94f44F7BdE028Cb58470dF5',
                # 'api': 'https://api.chat8.tech/v1',# https://api.openai.com/v1
                # 'key': 'sk-376bkdfy8FiC3Pyg108bF1A62b8e4b9aA85fE30eAd7635Eb',
                # 'api': 'https://api.foforise.xyz/v1',
                'proxy': '',  # http://127.0.0.1:21882
                'prompt': 'gpt-3.5-turbo-16k'
            }
            chat = ChatGPT(chargpt["key"], chargpt["api"], chargpt["proxy"], chargpt["prompt"])

            q = content
            rsp = chat.get_answer(q, wxid)
            print(rsp)

            cb = 'http://localhost:9999/text'
            data = {
                "msg": rsp,
                "receiver": wxid,
                "aters": '',
            }
            rsp = requests.post(url=cb, json=data, timeout=30)
            self.chengyu = ''
            print(rsp)
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

def run_schedule():
    while not stop_flag:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    #wx_http.weather_send()
    #exit(0)
    #wx_http.chengyu_send()

    #main()
    # exit(0)

    main_thread = threading.Thread(target=main, args=())

    # 创建定时任务线程
    schedule_thread = threading.Thread(target=schedule.every().day.at("07:00").do, args=(wx_http.weather_send,))
    schedule_thread.daemon = True

    # 设置停止标志
    stop_flag = False

    main_thread.start()
    schedule_thread.start()

    # 开启另一个线程执行定时任务
    schedule_run_thread = threading.Thread(target=run_schedule)
    schedule_run_thread.start()

    main_thread.join()

    # 停止定时任务线程
    stop_flag = True
    schedule_run_thread.join()

    # 创建定时任务线程
    # schedule_thread2 = threading.Thread(target=schedule.every().day.at("17:30").do, args=(wx_http.chengyu_send,))
    # schedule_thread2.start()