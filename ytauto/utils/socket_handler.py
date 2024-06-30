import socket
from pathlib import Path
import toml


config_file = Path(__file__).resolve().parents[1] / "config" / "socket.toml"
config = toml.load(config_file)


class SocketHandler:
    def __init__(self, ip: str):
        self.port = config["server"]["port"]
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def send(self, message: str) -> str:
        """发送消息，并收获返回数据"""
        try:
            self.client.send(message.encode())
        except ConnectionResetError:
            self.client.connect((self.ip, self.port))
            return self.send(message)
        recv = self.client.recv(1024)
        output = recv.decode()
        return output

    def start_chrome(self) -> str:
        """启动chrome"""
        return self.send("start_chrome")

    def stop_chrome(self) -> str:
        """关闭chrome"""
        return self.send("stop_chrome")

    def close(self):
        """关闭socket连接"""
        self.client.close()
            


        


