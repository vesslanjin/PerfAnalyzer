Intel Sample Source Code License

Copyright(c) 2015-2020 Intel Corporation. All rights reserved.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the distribution.
    * Neither the name of Intel Corporation nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# EMON 采集工具部署

### 安装包
- edp-v3.9.zip
- emon_nda_11_9_linux_05152019.tar.bz2

如有新版本，可使用新版本。


## 1 EMON 安装

```bash
# Linux 内核开发依赖环境安装
$ yum install kernel-devel
# EMON 安装
$ tar -jxvf emon_nda_11_9_linux_05152019.tar.bz2
$ unzip edp-v3.9.zip
$ cd emon_nda_11_9_linux_05152019
$ su                                         # 进入超级用户模式
$ sh install.sh
# 进入安装目录，重新编译驱动程序。（可能会有两个目录：/opt/intel/emon 和 /opt/intel/sep ，强烈推荐首选：/opt/intel/sep !!）
$ cd /opt/intel/sep/sepdk/src
$ ./build-driver
# 备注：如果运行 emon 时出现提示，如存在 pax 与 sep 冲突，请进入安装目录注销 pax 模块。命令如下：
# $ cd /opt/intel/sep/sepdk/src
# $ rmmod pax
```


## 2 EMON 运行脚本

- run_emon.sh
- stop_emon.sh

##### [run_emon.sh] （此处以 CascadeLake 2 Socket 的机器为例）
```bash
# 优先推荐：/opt/intel/sep 如果没有，则使用：/opt/intel/emon 目录下的 emon 程序。
SEP_DIR=/opt/intel/sep
DATA_DIR=$(dirname "$0")

mkdir -p ${DATA_DIR}/${1}
source ${SEP_DIR}/sep_vars.sh

${SEP_DIR}/sepdk/src/rmmod-sep
${SEP_DIR}/sepdk/src/insmod-sep

cp ${DATA_DIR}/chart_format_clx_2s.txt ${DATA_DIR}/${1}
cp ${DATA_DIR}/edp.rb ${DATA_DIR}/${1}
cp ${DATA_DIR}/clx-2s-events.txt ${DATA_DIR}/${1}
cp ${DATA_DIR}/process.sh ${DATA_DIR}/${1}
cp ${DATA_DIR}/clx-2s.xml ${DATA_DIR}/${1}

emon -v > ${DATA_DIR}/${1}/emon-v.dat
emon -M > ${DATA_DIR}/${1}/emon-M.dat
# 事件列表文件 xxx-xx-events.txt 由当前 cpu 架构决定
emon -i ${DATA_DIR}/${1}/clx-2s-events.txt > ${DATA_DIR}/${1}/emon.dat &
```

##### 注意
> - chart_*.txt、 *-events.txt、 *.xml （与架构相关：格式描述、事件列表、Metric公式） <br>
> - edp.rb、process.sh （Ruby脚本：根据 EMON 数据生成 CSV 文件）

以上五个文件均来源于 SEP 压缩包。

##### [stop_emon.sh]
```bash
# 注意，SEP_DIR 赋值同上
SEP_DIR=/opt/intel/sep
EMON_DIR=$(dirname "$0")
source ${SEP_DIR}/sep_vars.sh
emon -stop
```

##### [process.sh]
```bash
##ruby interpreter, change it according to the path where ruby is installed in your system
RUBY=ruby

##input file names, you may need to change them
EMON_DATA=emon.dat
EMON_V=emon-v.dat
EMON_M=emon-M.dat

##Workload related H/W and S/W configuration file; imported as-is into EDP spreadshe
CONFIG_FILE=config.xlsx

##Output of dmidecode; imported as-is into EDP spreadsheet
DMIDECODE_FILE=dmidecode.txt

##output of sar or other tool with network traffic
NETWORKSTAT_FILE=network.txt

##output of iostat or other tool with disk traffic
DISKSTAT_FILE=diskstat.txt

##output file name, you may want to change it

OUTPUT=summary.xlsx

##the metrics definition file; need to change this based on the architecture
METRICS=clx-2s.xml

##Excel chart format file, Need to change it based on the architecture
CHART_FORMAT=chart_format_clx_2s.txt

##the average value will be calculated from the %BEGIN% sample to %END% sample.
##setting %END% to a negative value means the last availabe sample.
BEGIN=1
END=1000000

VIEW="--socket-view --core-view --thread-view"

ruby edp.rb -i $EMON_DATA -j $EMON_V -k $EMON_M -g $CONFIG_FILE -d $DMIDECODE_FILE -D $DISKSTAT_FILE -n $NETWORKSTAT_FILE -f $CHART_FORMAT -o $OUTPUT -m $METRICS -b $BEGIN -e $END $VIEW $TPS $TIMESTAMP_IN_CHART

exit
```
注意，``METRICS、CHART_FORMAT`` 的内容需要根据实际情况替换。

```bash
$ yum install ruby
```
##### 特别提醒：强烈推荐使用 JRuby 的 process 脚本。 参考：``jruby_emon_process.md`` 内容。


## 3 目录结构

创建 emon 脚本的存放目录，如：``emon-scripts``。内部应包含以下文件：
- **chart_format_xxx_xx.txt**  （用于指定 csv 格式）
- **xxx-xx-events.txt** （采集事件的列表）
- **xxx-xx.xml** （公式计算列表）
- **edp.rb** （Ruby 脚本）
- **process.sh** （Ruby 脚本的调用程序）
- **run_emon.sh** （EMON 运行脚本）
- **stop_emon.sh** （EMON 结束脚本）

例如：
```
-rw-r--r-- 1 root root   885 Apr  2 17:13 chart_format_clx_2s.txt
-rw-r--r-- 1 root root 17439 Apr  2 17:13 clx-2s-events.txt
-rw-r--r-- 1 root root 84833 Apr  2 17:13 clx-2s.xml
-rw-r--r-- 1 root root 68508 Apr  2 17:13 edp.rb
-rwxr-xr-x 1 root root  1268 Apr  2 17:13 process.sh
-rwxr-xr-x 1 root root   571 Apr  2 17:13 run_emon.sh
-rwxr-xr-x 1 root root   106 Apr  2 17:13 stop_emon.sh
```

##### 测试

```bash
$ cd emon-scripts
$ bash run_emon.sh test
$ stop_emon.sh
```

```bash
$ cd emon-scripts/test
$ bash process.sh
```
