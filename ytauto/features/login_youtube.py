from playwright.sync_api import Page, Browser
from contextlib import contextmanager
from loguru import logger
from utils.base import Base
from pathlib import Path
from datetime import datetime


picture_dir = Path(__file__).resolve().parents[1] / "error_files"


def checker_loop(page: Page, browser: Browser, driver: Base):
    try:
        page.wait_for_url("https://www.youtube.com/", wait_until="load")
        logger.success("登录成功")
    except Exception as e:
        if "google.com/web/chip" in page.url:
            logger.success("登录成功")
            return
        elif "/signin/challenge/selection" in page.url:
            LoginVarify.varify_backup_email(page, browser, driver)
        elif "speedbump/gaplustos" in page.url:
            LoginVarify.varify_welcome_new_account(page, browser, driver)
        else:
            logger.error("进入未预设登录情况，登录失败")
            filename = datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".png"
            page.screenshot(path=(picture_dir / filename))
            raise AssertionError("进入未预设登录情况，登录失败")


class LoginVarify:
    @staticmethod
    def varify_backup_email(page: Page, browser: Browser, driver: Base):
        """验证备用邮箱步骤"""
        logger.info("开始验证备用邮箱")
        try:
            section = page.locator('li > div[role="link"] > div:last-child').nth(2)
            section.click()
            page.locator('#knowledge-preregistered-email-response').fill(driver.backup_email)
            buttons = page.locator("button").all()
            for btn in buttons:
                span = btn.locator("span")
                config_next_texts = list(driver.preconfig["login"]["next_button"].values())
                if span.text_content() in config_next_texts:
                    btn.click()
                    break
            checker_loop(page, browser, driver)
        except TimeoutError as e:
            logger.error("验证备用邮箱失败")
            raise AssertionError(f"验证备用邮箱失败")

    @staticmethod
    def varify_welcome_new_account(page: Page, browser: Browser, driver: Base):
        logger.info("开始处理新账号欢迎页")
        try:
            page.locator("#confirm").click()
            checker_loop(page, browser, driver)
        except Exception:
            logger.error("处理新账号欢迎页失败")
            raise AssertionError(f"处理账号欢迎页失败")



@contextmanager
def login_checker(page: Page, browser: Browser, driver: Base):
    yield
    page.wait_for_load_state("load")
    checker_loop(page, browser, driver)


    
