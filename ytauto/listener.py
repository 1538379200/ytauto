
#                              ╭──────────────────╮
#                              │ Socket服务端程序 │
#                              ╰──────────────────╯

import socket
import subprocess
import argparse
from loguru import logger
from pathlib import Path
import toml
from multiprocessing import Process
import os
from contextlib import suppress


run_bat = Path(__file__).parents[1] / "run.bat"
chrome_start_bat = Path(__file__).parents[1] / "start_chrome.bat"


document_path = Path("~/Documents/").expanduser() / "YTAuto" / "ytauto"
root_dir = Path(__file__).resolve().parent


config_file = Path(__file__).resolve().parent / "config" / "socket.toml"
config = toml.load(config_file)

port = config["server"]["port"]


parser = argparse.ArgumentParser(description="在当前设备启动SOCKET服务")

parser.add_argument("--host", type=str, required=True, help="填写当前设备的IP地址")

args = parser.parse_args()

host = args.host

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

sub_process: subprocess.Popen
chrome_process: subprocess.Popen


logger.info(f"启动监听，监听地址：{host}:{port}")
while True:
    client, addr = server.accept()
    recv = client.recv(1024).decode()
    # if recv == "start_chrome":
    #     logger.info(f"{addr}：启动chrome浏览器")
    #     sub_process = subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", "--remote-debugging-port=9527", "--incognito", "--start-maximized"], stdout=subprocess.PIPE)
    #     client.send("started".encode())
    # # 使用 "xx.xx.xx.xx test_end" 来发送
    # elif recv == "stop_chrome":
    #     logger.info(f"{addr}: 关闭chrome浏览器")
    #     try:
    #         sub_process.terminate()
    #         sub_process_two.terminate()
    #         client.send("OK".encode())
    #         logger.info("已关闭浏览器")
    #     except:
    #         client.send("没有需要关闭的chrome".encode())
    #         logger.info("没有需要关闭的chrome")
    if "start_chrome" in recv:
        chrome_process = subprocess.Popen(str(chrome_start_bat), stdout=subprocess.PIPE)
        logger.info(f"{addr}：启动chrome")
    elif "run" in recv:
        with suppress(Exception):
            chrome_process.terminate()
            sub_process.terminate()
            os.system("taskkill /im chrome.exe /f")
        chrome_process = subprocess.Popen(str(chrome_start_bat), stdout=subprocess.PIPE)
        scripts = recv.split(" ", 1)[-1].strip()
        logger.info(f"{addr}：执行脚本")
        sub_process = subprocess.Popen(f"{run_bat} {scripts}", stdout=subprocess.PIPE, cwd=str(root_dir))
        client.send("OK".encode())
    else:
        client.send("OK".encode())



