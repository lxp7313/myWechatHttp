#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import argparse

import uvicorn

from wcferry.client import Wcf, __version__
from wcferry.wxmsg import WxMsg
from wcfhttp.core import Http, __version__

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-v", "--version", action="version", version=f"{__version__}")
    parse.add_argument("--wcf_host", type=str, default=None, help="WeChatFerry 监听地址，默认本地启动监听 0.0.0.0")
    parse.add_argument("--wcf_port", type=int, default=10086,
                       help="WeChatFerry 监听端口 (同时占用 port + 1 端口)，默认 10086")
    parse.add_argument("--wcf_debug", type=bool, default=False, help="是否打开 WeChatFerry 调试开关")
    parse.add_argument("--host", type=str, default="0.0.0.0", help="wcfhttp 监听地址，默认监听 0.0.0.0")
    parse.add_argument("--port", type=int, default=9999, help="wcfhttp 监听端口，默认 9999")
    parse.add_argument("--cb", type=str, default="http://localhost:10000/msg_cb", help="接收消息回调地址")#http://localhost:9999/

    logging.basicConfig(level="INFO", format="%(asctime)s %(message)s")
    args = parse.parse_args()
    cb = args.cb
    if not cb:
        logging.warning("没有设置接收消息回调，消息直接通过日志打印；请通过 --cb 设置消息回调")
        logging.warning(f"回调接口规范参考接收消息回调样例：http://{args.host}:{args.port}/docs")
    wcf = Wcf(args.wcf_host, args.wcf_port, args.wcf_debug)
    home = "https://github.com/lich0821/WeChatFerry"
    qrcodes = """<table>
    <thead>
    <tr>
    <th style="text-align:center"><img src="https://raw.githubusercontent.com/lich0821/WeChatFerry/master/assets/TEQuant.jpg" alt="碲矿"></th>
    <th style="text-align:center"><img src="https://raw.githubusercontent.com/lich0821/WeChatFerry/master/assets/QR.jpeg" alt="赞赏"></th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td style="text-align:center">后台回复 <code>WeChatFerry</code> 加群交流</td>
    <td style="text-align:center">如果你觉得有用</td>
    </tr>
    </tbody>
    </table>"""
    http = Http(wcf=wcf,
                cb=cb,
                title="WeChatFerry HTTP 客户端",
                description=f"Github: <a href='{home}'>WeChatFerry</a>{qrcodes}", )

    uvicorn.run(app=http, host=args.host, port=args.port)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
