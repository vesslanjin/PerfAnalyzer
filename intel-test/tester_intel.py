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

#!/usr/bin/python
import os, sys
import json


######################
# utils
######################

def python_array_to_shell_array(arr):
    length = len(arr)
    ret = '('
    for idx, item in enumerate(arr):
        if idx < length - 1:
            ret = ret + '\"' + item + '\"' + ' '
        else:
            ret = ret + '\"' + item + '\"' + ')'
    return ret


######################
# tester
######################

def fetch_sku_info():
    temp_file = 'temp.info'
    cmd = 'lscpu > {}'.format(temp_file)
    os.system(cmd)
    sku_info = {}
    with open(temp_file, 'r') as f:
        for line in f:
            if 'Thread(s) per core:'.upper() in line.strip().upper():
                threads_per_core = line.strip().upper().split(':')[-1].strip()
                sku_info['threads_per_core'] = threads_per_core
            elif 'Core(s) per socket:'.upper() in line.strip().upper():
                cores_per_socket = line.strip().upper().split(':')[-1].strip()
                sku_info['cores_per_socket'] = cores_per_socket
            elif 'Socket(s):'.upper() in line.strip().upper():
                sockets = line.strip().upper().split(':')[-1].strip()
                sku_info['sockets'] = sockets
            elif 'Model name:'.upper() in line.strip().upper():
                sku = 'unkown'
                if 'Intel(R)'.upper() in line.strip().upper():
                    sku = line.strip().upper().split('CPU')[0].strip().split()[-1]
                elif 'AMD'.upper() in line.strip().upper():
                    sku = line.strip().upper().split('AMD')[-1].split()[1]
                sku_info['sku'] = sku
            elif 'L3 cache:'.upper() in line.strip().upper():
                llc_cache = line.strip().upper().split(':')[-1].strip()
                sku_info['llc_cache'] = llc_cache
    os.remove(temp_file)
    return sku_info


def parse_conf_file():
    conf_file = 'conf_intel.json'
    if not os.path.exists(conf_file):
        print('[Error]: <conf.json> file doesn\'t exist!')
        sys.exit(1)
    params = None
    with open(conf_file,'r') as f:
        conf = json.load(f)
        params = conf['config']
    return params


def run(params):
    sku_info = fetch_sku_info()
    sockets = sku_info['sockets']
    cores_per_socket = sku_info['cores_per_socket']
    threads_per_core = sku_info['threads_per_core']
    upper_id = int(sockets) * int(cores_per_socket) * int(threads_per_core) - 1
    # check
    cores_used = int(params['coresUsed'])
    max_cores = int(sockets) * int(cores_per_socket)
    if cores_used > max_cores:
        print('Error: <coresUsed> in conf.json beyond available range.')
        sys.exit(1)
    # python -> shell (os.environ for params passing)
    os.environ['env_llc_mask_scaling']=params['llcScaling']
    os.environ['env_llc_assoc']=params['llcAssoc']
    os.environ['env_core_freq_scaling']=params['coreFreqScaling']
    os.environ['env_uncore_freq_scaling']=params['uncoreFreqScaling']
    os.environ['env_memspeed']=params['memspeed']
    os.environ['env_emon_starttime']=str(params['emonStartTime'])
    os.environ['env_emon_duration']=str(params['emonDuration'])
    os.environ['env_sku']=sku_info['sku']
    os.environ['env_cores_used']=str(params['coresUsed'])
    os.environ['env_threads_used']=str(int(params['coresUsed'])*int(params['smt']))
    os.environ['env_workload_name']=params['workloadName']
    os.environ['env_smt']=str(params['smt'])
    # instances' informations (one or more determined by the list length)
    working_directory = []
    cmd_list = []
    numactl_list = []
    for instance in params['instances']:
        working_directory.append(instance['workingDirectory'])
        cmd_list.append(instance['cmd'])
        numactl_list.append(instance['numactl'])
    os.environ['env_working_directory'] = python_array_to_shell_array(working_directory)
    os.environ['env_cmd_list'] = python_array_to_shell_array(cmd_list)
    os.environ['env_numactl_list'] = python_array_to_shell_array(numactl_list)
    # run
    os.system('bash tester_intel.sh')
    

if __name__ == '__main__':
    params = parse_conf_file()
    run(params)
