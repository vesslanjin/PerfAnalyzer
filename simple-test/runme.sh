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

#!/usr/bin/bash

function run_instances ()
{
    declare -a workingd_list=${1}
    declare -a cmd_list=${2}
    declare -a numactl_list=${3}

    for idx in "${!cmd_list[@]}";
    do
        icmd=""
        numa=${numactl_list[$idx]}
        workingd=${workingd_list[$idx]}

        #echo $numa
        if [ "$numa" != "" ]; then
            icmd="numactl ${numactl_list[$idx]} ${cmd_list[$idx]} | tee -a result.log"
        else
            icmd="${cmd_list[$idx]} | tee -a result.log"
        fi

        ## goto working directory
        cd $workingd
        echo $(pwd)

        echo "${icmd}"
        eval "${icmd} &"
    done
}

function wait_instances ()
{
    declare -a cmd_list=${1}

    while true
    do
        end=true
        for icmd in "${cmd_list[@]}";
        do
            length=${#icmd}
            if [[ $length -gt 30 ]];
            then
                icmd=${icmd:0:30}
            fi

            res=`ps -ef | grep "${icmd}" | grep -v grep | wc -l`
            if [[ $res -gt 0 ]];
            then
                end=false
                break
            fi
        done

        if $end ;
        then
            break
        fi

        sleep "0.01"  # 10ms

    done
}

function wait_instances_with_timeout ()
{
    declare -a cmd_list=${1}
    timeout=${2}
    waittime=0

    while true
    do
        end=true
        for icmd in "${cmd_list[@]}";
        do
            length=${#icmd}
            if [[ $length -gt 30 ]];
            then
                icmd=${icmd:0:30}
            fi

            res=`ps -ef | grep "${icmd}" | grep -v grep | wc -l`
            if [[ $res -gt 0 ]];
            then
                end=false
                break
            fi
        done

        if $end ;
        then
            break
        fi

        waittime=`echo "$waittime + 1" | bc`
        sleep 1  # 1s
        #echo "waittime ${waittime}s timeout $timeout"

        if [ $(echo "${waittime} >= ${timeout}" | bc) == 1 ];
        then
            break
        fi

    done
}


# emon
emon_dir=/home/tools/emon-scripts

# host info
cores_per_socket=`lscpu |grep "Core(s) per socket:" | awk '{print $4}'`
sockets=`lscpu |grep "Socket(s):" | awk '{print $2}'`

# test result folder
data_folder=$(pwd)/data
mkdir -p $data_folder

# emon collection configs (unit: second)
emon_starttime=0
emon_duration=-1

# core freq scaling
#core_freq_scaling="(1.5 1.8 3.0)"
core_freq_scaling="(3.0)"
declare -a cpu_freq_scaling_list=$core_freq_scaling

# workload
workload_name="specjbb2015"
working_directory="(\"/home/aiyu/zhiheng/specjbb/SPECjbb2015\")"

# cmd
cmd="(\"bash run.sh.2 HBIR_RT jbb102 specjbb2015_pkb_baremetal jdk \"-XX:UseAVX=0\" NONE 0\")"
numactl="(\"-C 0-15,64-79 --localalloc\")"
cores_used=16
threads_used=32


## TestCase
for freq_idx in "${!cpu_freq_scaling_list[@]}";
do
    freq=`echo ${cpu_freq_scaling_list[$freq_idx]}*1000000 | bc | awk '{printf "%d", $0}'`
    echo "[-------- Core Freq --------]"
    echo "cpupower -c all frequency-set -d $freq -u $freq -g performance"
    cpupower -c all frequency-set -d $freq -u $freq -g performance

    # label of current case
    timets=$(date "+%Y%m%d%H%M")
    name="${workload_name}_${cores_per_socket}C${sockets}S_llc0x7ff_${cores_used}C${threads_used}T_core${cpu_freq_scaling_list
[$freq_idx]}_uncore2.4_mem2933_7702P_${timets}"
    echo $name

    # step1. startup instances at specified working directory
    # [Note: Will Change into New Direcotry]
    echo "[-------- instances --------]"
    run_instances "$working_directory" "$cmd" "$numactl"


    # step2. emon startup
    if [ $emon_duration -ne 0 ]; then
        echo "[-------- run emon --------]"
        sleep $emon_starttime
        bash ${emon_dir}/run_emon.sh $name
    fi

    # step3. wait
    if [ $emon_duration -gt 0 ]; then
        # timeout and then stop emon
        echo "[-------- wait $emon_duration s to stop emon. --------]"
        wait_instances_with_timeout "$cmd" "$emon_duration"
        bash ${emon_dir}/stop_emon.sh
        wait_instances "$cmd"
    elif [ $emon_duration -lt 0 ]; then
        # wait and then stop emon
        echo "[-------- emon: monitering the entire process. --------]"
        wait_instances "$cmd"
        bash ${emon_dir}/stop_emon.sh
    else
        # wait
        wait_instances "$cmd"
    fi


    echo $(pwd)
    if [ $emon_duration -gt 0 ] ; then
        mv *.log ${emon_dir}/${name}
    else
        mkdir -p ${emon_dir}/${name}
        mv *.log ${emon_dir}/${name}
    fi


    # custom content
    #mv jbb102/*jdk_specjbb2015* ${emon_dir}/${name}


    # data moving
    mv ${emon_dir}/${name} ${data_folder}

done


exit 0
