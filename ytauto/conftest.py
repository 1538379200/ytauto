import pytest
from ytauto.utils.base import Base
from loguru import logger
import os
import subprocess
from datetime import datetime
import time
from pathlib import Path
from ytauto.utils.sql_handler import sql
from ytauto.utils.socket_handler import SocketHandler


# ================================================ Common ====================================================

format_str = "%Y-%m-%dT%H-%M-%S"
log_name = datetime.now().replace(microsecond=0).strftime(format_str)
logger.add(f"./log/{str(log_name)}.log")
addr = ""


# ================================================= Hooks =====================================================

def pytest_addoption(parser: pytest.Parser):
    # parser.addoption(
    #     "--headless",
    #     default=False,
    #     action="store",
    #     type=bool,
    #     help="是否使用无头模式运行，无头模式不会打开浏览器执行"
    # )
    parser.addoption(
        "--debug-port",
        default=9527,
        action="store",
        type=int,
        help="指定debug浏览器启动的端口"
    )
    # parser.addoption(
    #     "--maximized",
    #     default=True,
    #     action="store",
    #     type=bool,
    #     help="是否使用最大化运行，仅在chrome浏览器中生效"
    # )
    # parser.addoption(
    #     "--chrome-path",
    #     default=None,
    #     action="store",
    #     help="指定chrome浏览器路径"
    # )
    # parser.addoption(
    #     "--base-url",
    #     default=None,
    #     action="store",
    #     help="选择根网址，后续路径将对此网址进行路径拼接"
    # )
    parser.addoption(
        "--word",
        default=None,
        action="store",
        help="自定义的搜索词"
    )
    parser.addoption(
        "--author",
        default=None,
        action="store",
        help="视频作者名称用于精准定位"
    )
    parser.addoption(
        "--account",
        default=None,
        action="store",
        help="设备登录Youtube的账号"
    )
    parser.addoption(
        "--password",
        default=None,
        action="store",
        help="设备登录Youtube的密码"
    )
    parser.addoption(
        "--email",
        default="",
        action="store",
        help="备用邮箱"
    )
    parser.addoption(
        "--lang",
        default="ko",
        action="store",
        help="选择对应的语言，在元素定位时，将进行区别使用，可选择 ko（韩语）、en（英语）"
    )
    parser.addoption(
        "--addr",
        default=None,
        action="store",
        help="当前执行的设备IP，外部传入，不进行自动获取"
    )
    parser.addoption(
        "--freq",
        default=2,
        action="store",
        type=int,
        help="关键词搜索次数"
    )
    parser.addoption(
        "--filter-types",
        default=None,
        action="store",
        help="需要进行过滤的搜索类型，多个以英文逗号分开"
    )
    parser.addoption(
        "--script-name",
        default="",
        action="store",
        help="当前执行的脚本名称"
    )


def remove_outdate_log():
    base_dir = Path("./log/").resolve()
    logs = base_dir.glob("*.log")
    logs = sorted(logs, key=lambda x: x.stat().st_atime, reverse=True)
    need_del_logs = logs[7:]
    for log in need_del_logs:
        log.unlink(missing_ok=True)


def close_all_chrome():
    os.system("taskkill /im chrome.exe /f")


def pytest_sessionstart(session: pytest.Session):
    logger.info("开始清理日志文件")
    remove_outdate_log()
    logger.info("删除错误截图")
    for f in Path("./error_files").resolve().glob("*"):
        f.unlink(missing_ok=True)


def pytest_configure(config: pytest.Config):
    global addr
    logger.info("添加执行设备数据")
    addr = config.getoption("--addr")
    if isinstance(addr, str):
        sql.insert_running_device(addr.strip(), 0)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    global addr
    out = yield
    result: pytest.TestReport = out.get_result()
    if result.when == "call":
        if isinstance(addr, str):
            if result.outcome == "passed":
                sql.change_running(addr, 1, "成功")
            else:
                exc_info = call.excinfo
                if exc_info is not None:
                    error = str(exc_info.value)
                else:
                    error = ""
                sql.change_running(addr, 2, error)

# ================================================ Fixture ======================================================

@pytest.fixture(autouse=True, scope="session", name="addr_ip")
def addr_ip(pytestconfig: pytest.Config):
    addr = pytestconfig.getoption("--addr")
    if isinstance(addr, str):
        return addr
    else:
        return ""


@pytest.fixture(autouse=True, scope="session", name="driver")
def init_base(pytestconfig: pytest.Config):
    endpoint_url = f"http://localhost:9527"
    logger.info(f"chrome地址：{endpoint_url}")
    search_word = pytestconfig.getoption("--word")
    author = pytestconfig.getoption("--author")
    email = pytestconfig.getoption("--account")
    pwd = pytestconfig.getoption("--password")
    backup_email = pytestconfig.getoption("--email")
    lang = pytestconfig.getoption("--lang")
    freq = pytestconfig.getoption("--freq")
    filter_types = pytestconfig.getoption("--filter-types")
    if filter_types is None:
        filter_types = []
    else:
        filter_types = [x.strip() for x in filter_types.split(",")]     # type: ignore
    if lang not in ("ko", "en"):
        raise RuntimeError(f"只能输入 ko、en")
    if search_word is None:
        logger.error(f"未填写搜索字符串，执行失败")
        pytest.exit()
    if pwd is None:
        logger.error(f"未填写登录密码，执行失败")
        pytest.exit()
    if author is None:
        logger.error(f"未填写油管视频作者名称，执行失败")
        pytest.exit()
    if email is None:
        logger.error(f"未填写登录邮箱地址，执行失败")
        pytest.exit()
    logger.info("开始连接chrome浏览器")
    base = None
    for _ in range(10):
        try:
            base = Base(
                endpoint_url=endpoint_url, 
                no_viewport=True,
                search_word=search_word,
                email=email,
                passwd=pwd,
                backup_email=backup_email,
                author=author,
                lang=lang,
                freq=freq,
                filter_types=filter_types 
            )
            break
        except Exception:
            time.sleep(1)
    if base is None:
        logger.error("执行出错，未连接到chrome，可能chrome未启动导致")
        raise RuntimeError(f"执行出错，未连接到chrome浏览器，可能连接未启动导致")
    yield base
    # base.close()


@pytest.fixture(name="page", scope="session")
def page(driver):
    return driver.page


@pytest.fixture(name="browser", scope="session")
def browser(driver):
    return driver.browser





