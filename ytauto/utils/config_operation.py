#                    ╭──────────────────────────────────────╮
#                    │           配置操作文件功能           │
#                    │ 文件尽量保持纯净，不借用其他文件内容 │
#                    │此文件将作为通用模块为其他模块提供功能│
#                    ╰──────────────────────────────────────╯
import toml
from pathlib import Path


class NodesHandler:
    """节点设备配置，默认为 config/nodes.toml 文件"""
    def __init__(self, config_file: str | Path | None = None):
        if config_file is None:
            self.config_file = Path(__file__).resolve().parents[1] / "config" / "nodes.toml"
        else:
            if isinstance(config_file, str):
                self.config_file = Path(config_file)
            else:
                self.config_file = config_file

    def read_conf(self):
        """
        读取配置文件数据
        """
        data = toml.load(self.config_file)
        return data
