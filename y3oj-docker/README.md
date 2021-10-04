# y³OJ Docker

[`memset0/y3oj-docker:1.0.0` - Docker Hub](https://hub.docker.com/layers/memset0/y3oj-docker/1.0.0/images/sha256-c198d89433c2e7a304feecef9421ba809a846434ffcd62b457c9b8d27d3b490c?context=repo)

## 本地构建

```
cp ../requirements.txt requirements.txt
docker build -t memset0/y3oj-docker:<tagname> .
docker push memset0/y3oj-docker:<tagname>  # publish to dockerhub
```

## 从 Docker Hub 拉取

```
docker pull memset0/y3oj-docker:<tagname>
```

也可以使用 `docker_pull.py` 脚本。

```
python docker_pull.py memset0/y3oj-docker:<tagname>
docker image load memset0_y3oj-docker.tar
```
