# Intel Sample Source Code License
#
# Copyright(c) 2015-2020 Intel Corporation. All rights reserved.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#     * Neither the name of Intel Corporation nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Plain Ordinary Python Objects
"""
import json

class CpiDetails(object):
    def __init__(self,workload=None,
                    sku=None,
                    cores=None,
                    threads=None,
                    llc=None,
                    memory_speed=None,
                    core_frequency=None,
                    uncore_frequency=None,
                    cpi=None,
                    computed_cpi=None,
                    cpi_error_rate=None,
                    cpu_util = None,
                    mips=None,
                    performance=None,
                    cores_per_socket=None,
                    evaluation=None,
                    eval_error_rate=None
                ):
        self.workload = workload
        self.sku = sku
        self.cores = cores
        self.threads = threads
        self.llc = llc
        self.memory_speed = memory_speed
        self.core_frequency = core_frequency
        self.uncore_frequency = uncore_frequency
        self.cpi = cpi
        self.computed_cpi = computed_cpi
        self.cpi_error_rate = cpi_error_rate
        self.cpu_util = cpu_util
        self.mips = mips
        self.performance = performance
        self.cores_per_socket = cores_per_socket
        self.evaluation = evaluation
        self.eval_error_rate = eval_error_rate

    def __repr__(self):
        return '<CpiDetails sku=%r cpi=%r cpu_util=%r cpi_error_rate=%r>' % (self.sku, self.cpi, self.cpu_util, self.cpi_error_rate)

    # 注意！ JSON.parse 解析的json字符串的内部必须使用双引号。
    def __str__(self):
        jstr = '"SKU": "{}", "CORES": "{}", "THREADS": "{}", "LLC_SIZE": "{}", "MEM_SPEED": "{}", "CORE_FREQ": "{}", \
            "UNCORE_FREQ": "{}", "CPI": "{}", "COMPUTED_CPI": "{}", "CPI_ERR": "{}", "CPU_UTIL": "{}", "MIPS": "{}", \
            "PERFORMANCE": "{}", "CORES_PER_SOCKET": "{}", "WORKLOAD": "{}", "EVALUATION": "{}", "EVAL_ERR_RATE": "{}" \
            '.format(
                self.sku, self.cores, self.threads, self.llc, self.memory_speed, self.core_frequency,
                self.uncore_frequency, self.cpi, self.computed_cpi, self.cpi_error_rate, self.cpu_util, self.mips,
                self.performance, self.cores_per_socket, self.workload, self.evaluation, self.eval_error_rate
            )
        return '{ ' + jstr + ' }'

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CpiDetails):
            return obj.__str__()
        if isinstance(obj, Sku):
            return obj.__str__()
        else:
            return super(MyEncoder, self).default(obj)


class Sku(object):
    def __init__(self,name=None,
                cores=None,
                uncore_frequency=None,
                llc_mb=None,
                turbo_core_frequency=None,
                base_core_frequency=None,
                tdp=None,
                price=None,
                turbo_performance=None,
                base_performance=None
            ):
        self.name = name
        self.cores = cores
        self.uncore_frequency = uncore_frequency
        self.llc_mb = llc_mb
        self.turbo_core_frequency = turbo_core_frequency
        self.base_core_frequency = base_core_frequency
        self.tdp = tdp
        self.price = price
        self.turbo_performance = turbo_performance
        self.base_performance = base_performance

    def __repr__(self):
        return '<Sku name=%r cores=%r uncore=%r llc=%rMB base=%r turbo=%r tdp=%r>' % (self.name,
            self.cores, self.uncore_frequency, self.llc_mb, self.base_core_frequency, self.turbo_core_frequency, self.tdp)

    def __str__(self):
        jstr = '"name": "{}", "cores": "{}", "uncore_frequency": "{}", "llc_mb": "{}", \
             "turbo_core_frequency": "{}", "base_core_frequency": "{}", "tdp": "{}", \
             "price": "{}", "turbo_performance": "{}", "base_performance": "{}"'.format(
                 self.name, self.cores, self.uncore_frequency, self.llc_mb,
                 self.turbo_core_frequency, self.base_core_frequency, self.tdp,
                 self.price, self.turbo_performance, self.base_performance
             )
        return '{ ' + jstr + ' }'
