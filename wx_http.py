from fastapi import Body, FastAPI, Request, Response
import uvicorn
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import requests

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
        if(wxid == 'wxid_mboc06esypzm19'):
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

wx_http = wx_http()
def main():
    app.add_api_route("/msg_cb", wx_http.msg_cb, methods=["POST"], summary="接收消息回调样例", tags=["示例"])

    uvicorn.run(app, host="localhost", port=10000)

if __name__ == '__main__':
    main()