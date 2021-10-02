# y³oj

> **DEVELOPING...**

It's (maybe) the first simple, light-weight and highly maintainable online judge system for secondary education.

一个简单、轻量化、易于部署的、为中学信息技术学科课业教学设计的 Online Judge 系统。

### 什么是 Online Judge

在线评测系统（英语：Online Judge，缩写 OJ）是一种在算法竞赛竞赛中用来测试参赛程序的在线系统，也可以用于平时练习。许多OJ网站会自发组织一些竞赛。此外，OJ网站通常会设立用户排名，以用户的提交答案通过数多少或某个题目执行时间快慢为排名依据。（[维基百科](https://zh.wikipedia.org/wiki/%E5%9C%A8%E7%BA%BF%E8%AF%84%E6%B5%8B%E7%B3%BB%E7%BB%9F)）

### 部署

* 复制 `./config.sample.yml` 到 `./config.yml` 并填写配置
* 从 [`y3oj/demo-data`](//github.com/y3oj/demo-data) 从下载示例数据到 `./data` 目录
* 运行以下代码

```shell
pip install -r requirements.txt
python build-frontend.py
python run.py
```

### 开发

#### 主程序 `y3oj`

使用 [Flask](https://flask.palletsprojects.com/en/2.0.x/) & [jinja2](https://jinja.palletsprojects.com/en/3.0.x/) 开发。

* 启动：`python ./run.py`。以开发模式启动，**请不要用于生产环境**。

#### 前端 `y3oj-frontend`

使用 [Less](https://lesscss.org/) 生成样式，使用 `build-frontend.py` 下载第三方包。

* 构建：`python ./build-frontend.py [--force]`。使用 `--force` 强制重新下载第三方包。
* Watch Mode：`python ./build-frontend.py --watch [--force]`。检测 `./y3oj-frontend` 的文件更改并自动重建。

#### 评测服务 `y3oj-judger`

咕咕咕。
