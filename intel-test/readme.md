# 测试环境搭建

#### 依赖
- Python3
- Bash Shell

### 1 Python 环境

- 推荐使用 ``virtualenv`` 创建隔离独立的 Python 环境。
- 使用 Python3 （2020 年 1 月之后，Python2 已停止维护。）

```bash
$ pip install virtualenv
$ virtualenv --no-site-packages venv -p python3
$ source venv/bin/activate
#$ deactivate
```

### 2 工具集部署

参考：[tools/readme.md](../tools/readme.md)
