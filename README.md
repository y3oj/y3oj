<h1 align="center">y³oj</h1>

<p align="center">
  It's (maybe) the first simple, light-weight and highly maintainable online judge system for secondary education.
  <br>
  一个简单、轻量化、易于部署的、为中学信息技术学科课业教学设计的 Online Judge 系统。
</p>

### Online Judge?

在线评测系统（Online Judge，缩写 OJ）是一种在算法竞赛竞赛中用来测试参赛程序的在线系统，也可以用于平时练习。许多 OJ 网站会自发组织一些竞赛。此外，OJ 网站通常会设立用户排名，以用户的提交答案通过数多少或某个题目执行时间快慢为排名依据。（来源：[维基百科](https://zh.wikipedia.org/wiki/%E5%9C%A8%E7%BA%BF%E8%AF%84%E6%B5%8B%E7%B3%BB%E7%BB%9F)）

该项目从传统 OJ 的设计出发，针对中学信息技术学科课业教学进行优化：如支持在 Python 中进行文件读取、引入第三方库等操作；同时原生支持交互式测评，并提供了一套 testlib API。

### Deploy

* 安装 **Python 3.8+**、**NodeJS 12+**，包管理库 pip、npm，命令行工具 wget、cmake。
* 复制 `./config.sample.yml` 到 `./config.yml` 并填写配置。**警告：务必填写 `secret_key` 为随机秘钥**。
* 从 [`y3oj/demo-data`](//github.com/y3oj/demo-data) 从下载示例数据到 `./data` 目录
* 评测端必须运行在 linux 环境下，请先配置 [@t123yh/simple-sandbox](https://github.com/t123yh/simple-sandbox) 所需的系统环境。

```bash
# 网页端
pip install -r requirements.txt
python build-frontend.py
python run.py
# 评测端
wget -c https://mirrors.tuna.tsinghua.edu.cn/archlinux/iso/latest/archlinux-bootstrap-2021.10.01-x86_64.tar.gz sandbox-chroot.tar.gz -O sandbox-chroot.tar.gz
sudo tar -zxvf sandbox-chroot.tar.gz -C {{config.judger.sandbox_chroot}}  # remember *sudo* && replace {{...}} with your configure
git clone https://github.com/t123yh/simple-sandbox.git  # repo mirror: https://e.coding.net/memset0/y3oj/simple-sandbox.git
cd simple-sandbox && CXX=clang++-9 yarn install && yarn run build && cd ..
npm install
```

### Usage

#### 主程序 `y3oj`

使用 [Flask](https://flask.palletsprojects.com/en/2.0.x/) & [jinja2](https://jinja.palletsprojects.com/en/3.0.x/) 开发。

* 启动：`python ./run.py`。以开发模式启动，**请不要用于生产环境**。

#### 前端 `y3oj-frontend`

使用 [Less](https://lesscss.org/) 生成样式，使用 `build-frontend.py` 下载第三方包。

* 构建：`python ./build-frontend.py [--force]`。使用 `--force` 强制重新下载第三方包。
* Watch Mode：`python ./build-frontend.py --watch [--force]`。检测 `./y3oj-frontend` 的文件更改并自动重建。

#### 评测服务 `y3oj-judger`

咕咕咕。
