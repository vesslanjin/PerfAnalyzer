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

# 约定规范

### 1 预定义规范

##### EMON 数据文件夹命名规范
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
示例：
    ffmpeg_18C2S_llc0x3f_8C16T_core2.1_uncore2.4_mem2933_6140_201911071309
```
