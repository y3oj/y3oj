# y³oj

> Developing...

It's (maybe) the first simple, light-weight and highly maintainable online judge system for secondary education.

一个简单、轻量化、易于部署的、为中学信息技术学科课业教学设计的 Online Judge 系统。

### Deploy

* clone 本仓库到本地目录 `.`
* 复制 `./config.sample.yml` 到 `./config.yml` 并填写配置
* 从 [`y3oj/demo-data`](//github.com/y3oj/demo-data) 从下载示例数据到 `./data` 目录
* 构建 `./y3oj-frontend` 目录下的静态文件，或从 [`y3oj/static-prebuild`](//github.com/y3oj/static-prebuild) 从下载示例数据到 `./static` 目录
* ```python
  pip install -r requirements.txt
	python run.py
	```