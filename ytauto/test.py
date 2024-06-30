import os
from pathlib import Path


file = Path(__file__).resolve().parents[1] / "start_chrome.bat"
os.system(str(file))
print("执行完成")


