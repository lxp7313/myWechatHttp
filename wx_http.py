from fastapi import Body, FastAPI, Request, Response
import uvicorn
from pydantic import BaseModel

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

async def msg_cb(Msg = Body(description="微信消息"), response= Response):
    print(f"收到消息：{Msg}")
    response.status_code = 300

    return {"status": 500, "message": "成功"}

app.add_api_route("/msg_cb", msg_cb, methods=["POST"], summary="接收消息回调样例", tags=["示例"])

uvicorn.run(app, host="0.0.0.0", port=10000)