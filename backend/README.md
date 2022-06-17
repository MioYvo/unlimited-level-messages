# 无限层级评论后端

### 目录结构

```text
backend/
       deploy/          # 部署相关
       flaskr/          # 源码
              utils/    
              views/    # 视图, API定义
       tests/           # 测试
```

### 一键部署
* 要求
  * [Docker Engine](https://docs.docker.com/engine/install/)
  * [Docker Compose](https://docs.docker.com/compose/)
  * localhost:80
  * 较快的网络连接
    * [Docker Hub](https://hub.docker.com/) 可用[阿里云加速地址](https://help.aliyun.com/document_detail/60750.html)
    * ~~Debian Sources~~ 已换用TUNA源
    * ~~PyPI~~ 已换用TUNA源
* 命令
  * Docker Desktop for Linux：
    ```shell
    cd recruitment-dev-python-backend-comments-tree-homework-RusiLiu
    docker-compose -f docker-compose.yml -p mio up -d --build --remove-orphans && firefox "http://localhost/index.html"
    ```
    
  * Docker Desktop for Mac：
    ```shell
    cd recruitment-dev-python-backend-comments-tree-homework-RusiLiu
    docker-compose -f docker-compose.yml -p mio up -d --build --remove-orphans && open "http://localhost/index.html"
    ```
    
  > 或`docker-compose`需要`sudu`执行
* 地址 [localhost:80](http://localhost/index.html)

### 测试
* local
  ```shell
  cd recruitment-dev-python-backend-comments-tree-homework-RusiLiu/backend/
  # create virtual env
  pip install -r deploy/requirements-dev.txt 
  pip install -e .
  pytest
  ```

* docker container
  ```shell
  cd recruitment-dev-python-backend-comments-tree-homework-RusiLiu/backend
  docker build -t test_backend -f deploy/test.Dockerfile .
  docker run -it --rm test_backend
  ```