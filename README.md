<br>

<h1 align="center">
  <img width="200" src="https://avatars.githubusercontent.com/u/91679741?s=200&v=4">
	<br>
	y³OJ
</h1>

<p align="center">
  (maybe the first) simple, light-weight and highly maintainable online judge system for secondary education.
  <br>
  一个简单、轻量化、易于部署的、为中学信息技术学科课业教学设计的 Online Judge 系统。
</p>

<br>

## Online Judge?

在线评测系统（Online Judge，缩写 OJ）是一种在算法竞赛竞赛中用来测试参赛程序的在线系统，也可以用于平时练习。许多 OJ 网站会自发组织一些竞赛。此外，OJ 网站通常会设立用户排名，以用户的提交答案通过数多少或某个题目执行时间快慢为排名依据。（来源：[维基百科](https://zh.wikipedia.org/wiki/%E5%9C%A8%E7%BA%BF%E8%AF%84%E6%B5%8B%E7%B3%BB%E7%BB%9F)）

该项目从传统 OJ 的设计出发，针对中学信息技术学科课业教学进行优化：如支持在 Python 中进行文件读取、引入第三方库等操作；同时原生支持交互式测评，并提供了一套 testlib API。

<br>

## Deploy

#### 准备工作

* 安装 **Python 3.8+**、**NodeJS 12+**，包管理库 pip、npm，命令行工具 wget、cmake。
* 复制 `./config.sample.yml` 到 `./config.yml` 并填写配置。**警告：务必填写 `secret_key` 为随机秘钥**。
* 从 [@y3oj/demo-data](//github.com/y3oj/demo-data) 从下载示例数据到 `./data` 目录。
* 评测端必须运行在 linux 环境下，请配置 [@t123yh/simple-sandbox](https://github.com/t123yh/simple-sandbox) 所需的系统环境。

#### 网页端

```bash
pip install -r requirements.txt
python build-frontend.py
python run.py
```

#### 评测端

```bash
cd y3oj-judger
git clone https://github.com/t123yh/simple-sandbox.git  # repo mirror: https://e.coding.net/memset0/y3oj/simple-sandbox.git
cd simple-sandbox && CXX=clang++-9 yarn install && yarn run build && cd ..
npm install
npm run judge-test  # run test
npm run judge-start
```

#### Sandbox

```bash
wget -c https://mirrors.tuna.tsinghua.edu.cn/archlinux/iso/latest/archlinux-bootstrap-2021.10.01-x86_64.tar.gz -O sandbox-rootfs.tar.gz
mkdir -p /path/to/sandbox-rootfs  # `/path/to/sandbox-rootfs/root.x86_64` should be `config.judger.sandbox_rootfs`
sudo tar -zxvf sandbox-rootfs.tar -C /path/to/sandbox-rootfs  # remember `sudo`
cd /path/to/sandbox-rootfs
mount ./root.x86_64/ ./root.x86_64/ --bind
mkdir -p /sandbox/working
groupadd --gid 725 y3oj && useradd --uid 725 --gid y3oj --shell /bin/bash --create-home y3oj
sudo ./root.x86_64/usr/bin/arch-chroot ./root.x86_64/
echo "Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/\$repo/os/\$arch" > /etc/pacman.d/mirrorlist
pacman -Syy
pacman-key --init && pacman-key --populate archlinux
pacman -S python3 python-pip --noconfirm
pip install flask numpy matplotlib pandas flask_wtf requests pyyaml flask_login --index-url https://pypi.douban.com/simple
```

<br>

## Usage

#### 主程序 `y3oj`

使用 [Flask](https://flask.palletsprojects.com/en/2.0.x/) & [jinja2](https://jinja.palletsprojects.com/en/3.0.x/) 开发。

* 启动：`python ./run.py`。以开发模式启动，**请不要用于生产环境**。

#### 前端 `y3oj-frontend`

使用 [Less](https://lesscss.org/) 生成样式，使用 `build-frontend.py` 下载第三方包。

* 构建：`python ./build-frontend.py [--force]`。使用 `--force` 强制重新下载第三方包。
* Watch Mode：`python ./build-frontend.py --watch [--force]`。检测 `./y3oj-frontend` 的文件更改并自动重建。

#### 评测服务 `y3oj-judger`

使用 [NodeJS] 开发，沙盒由 [@t123yh/simple-sandbox](https://github.com/t123yh/simple-sandbox) 提供。

* 启动：`node y3oj-judger/main.js`
* 测试：`node y3oj-judger/test_judger.js`