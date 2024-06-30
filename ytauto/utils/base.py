from playwright.sync_api import sync_playwright
from contextlib import suppress
from typing import Any
import toml
from pathlib import Path


class SpecialElements:
    ...

class Base:
    """基础方法，用于实例化浏览器配置"""
    def __init__(self, endpoint_url: str, no_viewport: bool | None, search_word: Any, email: Any, passwd: Any, backup_email: Any, author: Any, lang: Any, freq: Any, filter_types: list):
        config_file = Path(__file__).resolve().parents[1] / "config" / "special_elements.toml"
        self.base_url = "http://www.youtube.com"
        self.__pw = sync_playwright().start()
        self.browser = self.__pw.chromium.connect_over_cdp(endpoint_url=endpoint_url)
        self.context = self.browser.contexts[0] if self.browser.contexts else self.browser.new_context(no_viewport=no_viewport)
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.filter_types = filter_types
        self.lang=lang
        self.freq = freq
        self.search_word = search_word
        self.account = email
        self.password = passwd
        self.backup_email = backup_email
        self.author = author
        self.preconfig = toml.load(config_file)



    # def close(self):
    #     with suppress(Exception):
    #         self.page.close()
    #     with suppress(Exception):
    #         self.context.close()
    #     with suppress(Exception):
    #         self.browser.close()
    #     with suppress(Exception):
    #         self.__pw.stop()


