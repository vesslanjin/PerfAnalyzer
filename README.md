# Performance Analyzer

## 1 开发环境部署

### 1.1 安装 node.js 环境
官网 http://nodejs.org/ ，下载安装即可。

```bash
node -v
```

### 1.2 安装 Vue.js 运行环境

Vue.js 是一个基于 JavaScript 语言的前端渲染框架。
```bash
npm set registry http://registry.npm.taobao.org                      #切换为淘宝源
npm install -g vue-cli@2.9                                           #安装vue.js 2.9版本
npm list -g --depth 0                                                #查看已安装的工具包
cd frontend/
npm install                                                          #安装package.json文件内所列举的js依赖库
npm run dev                                                          #运行。Ctrl+C 结束
```

### 1.3 后端环境搭建（Python3）

使用 virtualenv 创建独立的 python 运行环境。（用于防止环境污染，非常推荐！）

```bash
pip install virtualenv                                               #安装 virtualenv
virtualenv --no-site-packages venv -p python3                        #创建一个venv目录，存放隔离环境
source venv/Scripts/activate                                         #windows系统下的bash命令（gitbash）
#.\venv\Scripts\activate                                             #windows系统下的cmd命令
source venv/bin/activate                                             #linux系统下的命令
deactivate                                                           #退出虚拟环境
```

安装
```bash
source venv/bin/activate
pip install numpy==1.17.0
pip install PyMySQL==0.9.3
pip install SQLAlchemy==1.3.5
pip install scipy==1.3.0
pip install scikit-learn==0.21.3
pip install Flask==1.0.3
pip install Flask-Cors==3.0.8
pip install Flask-SQLAlchemy==2.4.0
```

## 2 运行

```bash
source venv/bin/activate
cd backend
python view.py
```

```bash
cd client 
npm run dev 
```

打开浏览器，访问 ``http://localhost:8080``。

<br>

# 2 发布版（release）

### 2.1 编译 Vue 项目
```bash
cd frontend/
npm run build
```
编译之后，会在 dist 目录下生成 ``index.html`` 以及 ``static`` 目录。

### 2.2 将静态资源添加至 Flask 后端
1. ``cd backend``，在 backend 目录下创建 ``templates`` 目录，并将 ``index.html`` 拷贝至 templates 目录。
2. 将 ``static`` 目录连同内部文件，拷贝至 backend 目录。

### 2.3 测试
```bash
cd backend
python view.py
```
打开浏览器，访问 ``http://localhost:5000`` 。

<br>

# 自动化测试

> 注意：EMON 文件的命名规范是连接自动化测试和数据分析工具的桥梁！

### EMON 数据文件夹命名规范

```
命名规则：
    workload_xxCxxS_llcxx_xxCxxT_corexx_uncorexx_memxx_sku_xxxxxxxx(日期)
参数说明：
    1. workload —— workload 信息（自定义，例： ffmpeg）
    2. xxCxxS —— Cores/Skt Skts
        (例如： Xeon 6140 的机器 —— 18C2S
            Core(s) per socket:   18
            Socket(s):             2
        )
    3. llcxx —— LLC Size （用户根据实际情况填写，如： llc0x3f）
    4. xxCxxT —— 测试实际使用核心数和线程数 （如： 8核16线程 8C16T）
    5. corexx —— cpu freq (例： core2.1)
    6. uncorexx —— uncore freq （例： uncore2.4）
    7. memxx —— memory speed （例： mem2933）
    8. sku —— CPU 代号 （例： 6140）
    9. xxxx(日期) —— 测试日期 （例： 201911071309 年月日时分）
示例：ffmpeg_18C2S_llc0x3f_8C16T_core2.1_uncore2.4_mem2933_6140_201911071309
```

### 测试脚本

- 简单测试：simple-test
- Scaling 测试（Intel）：intel-test

### Contactor
- Wang, Zhiheng 
- Jin, Jun (jun.i.jin@intel.com)
- Han, Qiufeng (qiufeng.han@intel.com)
- Sun, Xingyi (xingyi.sun@intel.com)

