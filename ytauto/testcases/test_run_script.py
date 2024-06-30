from playwright.sync_api import Browser, Page, Locator
from loguru import logger
from ytauto.utils.base import Base
import pytest
from ytauto.features.login_youtube import login_checker


class Templates:
    @staticmethod
    def temp_search_live(driver: Base):
        """搜索直播"""
        base_url = driver.base_url
        page = driver.page
        logger.info(f"搜索直播：{driver.search_word}")
        page.goto(base_url + f"/results?search_query={driver.search_word}&sp=EgJAAQ%253D%253D")
        page.wait_for_load_state("load")

    @staticmethod
    def temp_filter_types(driver: Base, filter_words: list[str]):
        """进行多重过滤操作"""
        page = driver.page
        for filter_word in filter_words:
            is_found = False
            logger.info(f"过滤类型：{filter_word}")
            filter_btn = page.locator('xpath=//div[@id="filter-button"]//button')
            filter_btn.click()
            # filter_dialog = page.get_by_role("dialog")
            filter_dialog = page.locator("tp-yt-paper-dialog").first
            filter_dialog.wait_for(state="visible")
            filter_links = filter_dialog.locator('xpath=//a[@id="endpoint"]').all()
            for link in filter_links:
                filter_label = link.locator("xpath=//yt-formatted-string").text_content()
                if filter_label is not None and filter_label in filter_word:
                    is_found = True
                    link.click()
                    page.wait_for_load_state("load")
                    page.wait_for_timeout(500)
                    break
            if is_found is False:
                logger.error(f"未找到过滤项：{filter_word}")

    @staticmethod
    def temp_filter_need_live(driver: Base, sections: list[Locator]) -> bool:
        """
        进行直播间过滤操作
        """
        for section in sections:
            dismissbles = section.locator('xpath=//div[@id="dismissible"]').all()
            logger.info(f"查找账号：{driver.author}")
            for channel in dismissbles:
                author_name = channel.locator('xpath=//div[@id="channel-info"]//yt-formatted-string/a').text_content()
                if driver.author in author_name:
                    title = channel.locator('xpath=//a[@id="video-title"]')
                    title.scroll_into_view_if_needed()
                    title.click()
                    logger.success(f"已找到直播间并成功进入，直播间名称：{title.text_content()}")
                    return True
        else:
            return False

    @staticmethod
    def temp_check_is_page_end(driver: Base, sections: list[Locator]):
        """检查是否已翻页到最底部"""
        for section in sections:
            child_tag = section.locator('xpath=//div[@id="contents"]/*').first
            child_tag_name = child_tag.evaluate("el => el.tagName")
            if child_tag_name is not None and "ytd-message-renderer" in child_tag_name.lower():
                logger.info("已翻阅至最底部")
                return True
        else:
            return False

    @staticmethod
    def temp_scroll_to_end(driver: Base):
        page = driver.page
        scoll_hight = 0
        cheked_sections_num = 0
        while True:
            scoll_hight = page.evaluate('document.querySelector("#page-manager").scrollHeight')
            page.evaluate("(height) => window.scrollTo(0, height)", scoll_hight)
            page.wait_for_timeout(2000)
            channel_sections = page.locator("ytd-item-section-renderer").all()
            try:
                section = channel_sections[cheked_sections_num]
            except IndexError:
                logger.info(f"已查找 {cheked_sections_num + 1} 页")
                return False
            result = Templates.temp_filter_need_live(driver, [section])
            if result is True:
                logger.info(f"已查找 {cheked_sections_num + 1} 页")
                return True
            else:
                if Templates.temp_check_is_page_end(driver, [section]):
                    logger.info(f"已查找 {cheked_sections_num + 1} 页")
                    return False
                else:
                    cheked_sections_num += 1

    @staticmethod
    def temp_main(driver: Base) -> bool:
        """搜索主要执行方法，返回布尔值，是否已找到并进入直播间"""
        for _ in range(driver.freq):
            # 搜索
            Templates.temp_search_live(driver)
            # 过滤
            Templates.temp_filter_types(driver, driver.filter_types)
            # 滚动筛选
            result = Templates.temp_scroll_to_end(driver)
            if result is True:
                return True
        return False

    @staticmethod
    def is_logged(driver: Base):
        ...


class TestRunScript:
    @pytest.mark.live
    def test_search_youtube_live(self, page: Page, browser: Browser, driver: Base):
        base_url = "http://www.youtube.com"
        logger.info("进入youtube地址")
        page.goto(base_url)
        # 获取页面中所有的登录按钮
        login_btn = page.locator('div[id="end"] > div[id="buttons"] > ytd-button-renderer > yt-button-shape > a')
        logger.info("点击登录按钮，跳转Google登录")
        login_btn.click()
        with login_checker(page, browser, driver):
            # 进行账号输入操作
            logger.info(f"输入邮箱账号：{driver.account}")
            account_input = page.locator("input[name='identifier']")
            account_input.clear()
            account_input.fill(driver.account)
            # 点击下一步
            page.locator("div[id='identifierNext'] > div > button").click()
            # 进行密码输入
            logger.info(f"输入密码：{driver.password}")
            pwd_input = page.locator("input[name='Passwd']")
            pwd_input.clear()
            pwd_input.fill(driver.password)
            # 进行下一步操作
            page.locator("div[id='passwordNext'] > div > button").click()
        result = Templates.temp_main(driver)
        assert result is True, f"未找到属于账号 {driver.author} 的直播间数据"
                


        

                

        
