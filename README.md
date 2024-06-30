# YTAuto使用说明

## 执行环境配置

> 执行环境配置当前说明为手动操作版说明，如果为自动环境部署，你仅需要安装 `python3.12` 、`OpenSSH` 、`Chrome` 、`Bandizip` ，此处不涉及远程操控，仅执行端执行环境部署和执行操作

- 安装 `python3.12` ，安装后打开 `cmd` 命令行，输入 `python --version` 确认安装成功

- 安装 `poetry` 虚拟环境管理工具，在 `cmd` 执行命令:
  
  ```bash
  # 能正常访问外网执行此命令即可
  pip install poetry
  # 仅国内网络需要执行此命令提升安装速度和稳定性
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple poetry
  ```

- 进入项目文件夹（未修改为 `YTAuto` 文件夹），打开 `cmd` ，执行命令 `poetry install` 安装项目依赖（如果项目中带有整体虚拟环境，可以省略此步骤，即项目中包含 `.venv` 文件夹）

- 安装 `chrome` 浏览器，建议默认路径安装，默认路径一般为 `C:\Program Files\Google\Chrome\Application\chrome.exe`

- 进入文件夹 `ytauto` （`YTAuto` 下的子文件夹），在文件夹中，执行命令：

```bash
poetry run pytest --account=xxx --password=xxx --email=xxx --word=xxx --author=xxx --addr=xxx
```

- 必要参数：
  
  - `--account`：`youtube` 登录账号
  
  - `--password`：`youtube` 账号登录密码
  
  - `--email`：`youtube` 账号登录备用邮箱
  
  - `--word`：在 `youtube` 中搜索使用的关键词
  
  - `--author`：需要进行筛选的直播/视频作者
  
  - `--addr`：执行设备的 `IP`

- 其他参数：
  
  - `--chrome-path`：如果你的 `Chrome` 安装非上述的默认路径，则需要指定 `chrome.exe` 所在路径，注意路径需包括 `chrome.exe` 
  
  - `--lang`：指定当前执行的语言环境
  
  - `--debug-port`：指定启动 `debug` 浏览器的端口
