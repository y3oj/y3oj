
<img align="right" width="200" src="https://avatars.githubusercontent.com/u/91679741?s=200&v=4">

# y³OJ

![](https://tokei.rs/b1/github/y3oj/y3oj)

a simple, light-weight and highly maintainable online judge system for secondary education
  
一个简单、轻量化、易于维护的、为中学信息技术学科课业教学设计的 Online Judge 系统。

### Online Judge?

在线评测系统（Online Judge，缩写 OJ）是一种在算法竞赛竞赛中用来测试参赛程序的在线系统，也可以用于平时练习。许多 OJ 网站会自发组织一些竞赛。此外，OJ 网站通常会设立用户排名，以用户的提交答案通过数多少或某个题目执行时间快慢为排名依据。（来源：[维基百科](https://zh.wikipedia.org/wiki/%E5%9C%A8%E7%BA%BF%E8%AF%84%E6%B5%8B%E7%B3%BB%E7%BB%9F)）

该项目从传统 OJ 的设计出发，针对中学信息技术学科课业教学进行优化：如支持在 Python 中进行文件读取、引入第三方库等操作；同时原生支持交互式测评，并提供了一套 testlib API。

### Deploy

#### 环境配置

由于 Sandbox 技术限制，评测端必须部署在 Linux 中。环境需求如下：

* Python 3.6+
* NodeJS 12+
* 包管理器 pip & npm
* 命令行工具 wget & cmake

配置文件为 `./config.yml`，请复制 `./config.sample.yml` 到 `./config.yml` 并填写配置。为了网站安全，请**务必填写 `secret_key` 选项为随机秘钥**，登录插件等都依赖于此。

数据目录为 `./data`，你可以从 [@y3oj/demo-data](//github.com/y3oj/demo-data) 从下载示例数据。

为运行 Sandbox 请按照 [@t123yh/simple-sandbox](https://github.com/t123yh/simple-sandbox) 配置系统。

#### 网页端

使用 [Flask](https://flask.palletsprojects.com/en/2.0.x/) & [jinja2](https://jinja.palletsprojects.com/en/3.0.x/) 开发，需要安装相关依赖。

```bash
pip install -r requirements.txt
python build-frontend.py
python run.py      # start server
```

#### 前端

使用 [Less](https://lesscss.org/) 生成样式，第三方包托管在 [@y3oj/thirdparty-host](//github.com/y3oj/thirdparty-host)。

```bash
npm install -g less uglifyjs
python build-frontend.py      # build static
```

`build-frontend.py` 提供两个参数：

* `--force`，构建时强制重新下载第三方包，复制静态文件时强行覆盖。
* `--watch`，启用 Watch Mode，依赖于系统 API 检测文件更改时自动重新构建。

#### 评测端

使用 [NodeJS](https://nodejs.org/en/) 开发，沙盒由 [@t123yh/simple-sandbox](https://github.com/t123yh/simple-sandbox) 提供，使用 [websocket](https://github.com/websockets/ws) 与主程序通信。

再次提醒，请确保已经按照 [@t123yh/simple-sandbox](https://github.com/t123yh/simple-sandbox) 配置系统。

```bash
cd y3oj-judger
git clone https://github.com/t123yh/simple-sandbox.git  # repo mirror: https://e.coding.net/memset0/y3oj/simple-sandbox.git
cd simple-sandbox && CXX=clang++-9 yarn install && yarn run build && cd ..
npm install
npm run judge-test      # run test
npm run judge-start     # start judge server
```

#### Sandbox Rootfs

另外需要构建一个沙盒所使用的 rootfs。这里用的是 archlinux，参考代码如下

```bash
wget -c https://mirrors.tuna.tsinghua.edu.cn/archlinux/iso/latest/archlinux-bootstrap-2021.10.01-x86_64.tar.gz -O sandbox-rootfs.tar.gz
mkdir -p ./sandbox-rootfs
sudo tar -zxvf sandbox-rootfs.tar.gz -C ./sandbox-rootfs  # remember `sudo`
cd ./sandbox-rootfs
mount ./root.x86_64/ ./root.x86_64/ --bind
sudo ./root.x86_64/usr/bin/arch-chroot ./root.x86_64/
mkdir -p /sandbox/working
echo "Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/\$repo/os/\$arch" > /etc/pacman.d/mirrorlist
pacman -Syy
pacman-key --init && pacman-key --populate archlinux
pacman -S python3 python-pip --noconfirm
pip install flask numpy matplotlib pandas flask_wtf requests pyyaml flask_login --index-url https://pypi.douban.com/simple
```

### Docs

请访问 [y3oj-docs](https://github.com/y3oj/y3oj/tree/main/y3oj-docs)。