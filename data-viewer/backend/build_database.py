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

# encoding:utf-8
import os, sys, csv, math
import subprocess

from dao import init_db, db_session
from dao import Config, Emon, Cpi


####################################
# Emon Data and Performance Data
####################################

def load_data_from_rootdir(rootdir):
    """
    @param rootdir: directory contains many emon data dirs.
    """
    for root, dirs, files in os.walk(rootdir):
        for folder in dirs:
            print("processing..", folder)
            emon_data_folder_path = os.path.join(rootdir, folder)
            load_emon_data_by_csv(emon_data_folder_path)
            load_perfromance_data_by_shell(emon_data_folder_path)
        break

def load_emon_data_by_csv(dirpath):
    label = os.path.split(dirpath)[-1]
    # Hint!! __edp_socket_view_summary.csv
    filename = "__edp_socket_view_summary.csv"
    csvfile = os.path.join(dirpath, filename)
    if os.path.exists(csvfile):
        print("[csv]: ", filename)
        item = Emon.query.filter(Emon.label == label).first()
        if item is None:
            for emon_data in read_csv(csvfile):
                emon_data.label = label
                db_session.add(emon_data)
            db_session.commit()
        else:
            pass
    else:
        emon_data = Emon()
        emon_data.label = label
        db_session.add(emon_data)
        db_session.commit()

def read_csv(csvfile):
    with open(csvfile) as f:
        reader = csv.reader(f)
        # 1.首行，获取socket信息。
        first_row = next(reader)
        skts = len(first_row) - 1
        # 2.Emon对象初始化，用于数据封装。
        obj_list = []
        for i in range(skts):
            emon = Emon()
            emon.socket = first_row[i + 1].strip().upper()
            obj_list.append(emon)
        # 3.更新 cpu_freq、mem_speed、uncore_freq、cpu_util、llc_mpi、llc_mpns、cpi
        for row in reader:
            if "metric_CPU operating frequency (in GHz)".upper() in row[0].strip().upper():
                for i in range(skts):
                    obj_list[i].cpu_freq = float(row[i + 1].strip())
            elif "metric_DDR data rate (MT/sec)".upper() in row[0].strip().upper():
                for i in range(skts):
                    obj_list[i].mem_speed = float(row[i + 1].strip())
            elif "metric_uncore frequency GHz".upper() in row[0].strip().upper():
                for i in range(skts):
                    obj_list[i].uncore_freq = float(row[i + 1].strip())
            elif "metric_CPU utilization".upper() in row[0].strip().upper():
                if "kernel mode".upper() in row[0].strip().upper():  # ignore the kernel mode
                    continue
                for i in range(skts):
                    obj_list[i].cpu_util = float(row[i + 1].strip())
            elif "metric_LLC MPI (includes code+data+rfo w/ prefetches)".upper() in row[0].strip().upper():
                for i in range(skts):
                    obj_list[i].llc_mpi = float(row[i + 1].strip())
            elif "metric_Average LLC data read (demand+prefetch) miss latency (in ns)".upper() in row[0].strip().upper():
                for i in range(skts):
                    obj_list[i].llc_mpns = float(row[i + 1].strip())
            elif "metric_CPI".upper() in row[0].strip().upper():
                for i in range(skts):
                    obj_list[i].cpi = float(row[i + 1].strip())
        return obj_list

def load_perfromance_data_by_shell(dirpath):
    label = os.path.split(dirpath)[-1]
    # Hint!! 'performance.sh' for Performance Parsing!
    shellname = "performance.sh"
    bashfile = os.path.join(dirpath, shellname)
    if os.path.exists(bashfile):
        performance = run_bashshell(bashfile)
        print("[shell]: {0}, Performance: {1}".format(shellname, performance))
        items = Emon.query.filter(Emon.label == label).all()
        for item in items:
            item.performance = performance
        db_session.commit()
    else:
        pass

def run_bashshell(bashfile):
    twd = os.path.dirname(bashfile)           #Target Working Directory
    cwd = os.getcwd()                         #Current Working Directory
    filename = os.path.split(bashfile)[-1]
    os.chdir(twd)
    result = subprocess.getoutput('bash {}'.format(filename))
    os.chdir(cwd)
    return result


####################################
# Configuration Info
# label 规范：workload_xxCxxS_llcxx_xxCxxT_corexx_uncorexx_memxx_sku_xxxxxxxx(日期)
####################################

def update_tb_config():
    # Hint!! 目前，默认使用 Socket 0 的 emon 数据，因为当前做分析只使用一块CPU。
    emons = Emon.query.filter(Emon.socket == 'socket 0'.upper()).all()
    if len(emons) < 1:
        emons = Emon.query.all()
    # Traverse tb_emon
    for emon in emons:
        lgroups = emon.label.upper().split('_')
        workload = lgroups[0]
        sku = lgroups[7]
        cores = int(lgroups[3].split('C')[0])
        threads = int(lgroups[3].split('C')[-1].split('T')[0])
        smt = str(threads/cores)
        memory_speed = lgroups[6].split('MEM')[-1]
        llc = lgroups[2].split('C')[-1]
        core_frequency = lgroups[4].split('CORE')[-1]
        uncore_frequency = lgroups[5].split('CORE')[-1]
        cores = str(cores)
        if emon.mem_speed is not None:
            memory_speed = str(math.floor((emon.mem_speed+50)/100)*100)
        if emon.cpu_freq is not None:
            core_frequency = str(round(emon.cpu_freq, 1))
        if emon.uncore_freq is not None:
            uncore_frequency = str(round(emon.uncore_freq, 1))
        config = Config(workload=workload,
                 sku=sku,
                 smt=smt,
                 memory_speed=memory_speed,
                 llc=llc,
                 cores=cores,
                 core_frequency=core_frequency,
                 uncore_frequency=uncore_frequency)
        existing = Config.query.filter_by(workload=workload,
                 sku=sku,
                 smt=smt,
                 memory_speed=memory_speed,
                 llc=llc,
                 cores=cores,
                 core_frequency=core_frequency,
                 uncore_frequency=uncore_frequency).first()
        if not existing:
            db_session.add(config)
            db_session.flush()                                                   #用于返回新增的id
            db_session.commit()                                                  #此时数据才插入到数据库中
        else:
            config = existing
        emon.config_id = config.id
    db_session.commit()                                                          #再次commit，更新emon的config_id



if __name__ == '__main__':
    init_db()
    test_result_rootdir = '../../../data/emon_result'
    load_data_from_rootdir(test_result_rootdir)
    update_tb_config()
