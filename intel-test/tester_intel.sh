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

# tools: emon, setCpuFRE, RDT
tools=$(pwd)/../tools
emon_dir=${tools}/emon-scripts
setcpu_freq_dir=${tools}/setCpuFRE
rdt_path=${tools}/intel-cmt-cat

# config scaling params
llc_mask_scaling=(0x3f)
core_freq_scaling=(2.1)
uncore_freq_scaling=(2.4)
llc_assoc="0,2,4,6-10"

# infos of instances
workload_name="test"
working_directory=("./" "./")
cmd=("sh test.sh" "sh test.sh")
numactl=("-C 0-23,48-71" "-C 24-47,72-95")

# emon configs (unit: second)
emon_starttime=0
emon_duration=30

# host info
cores_per_socket=`lscpu |grep "Core(s) per socket:" | awk '{print $4}'`
sockets=`lscpu |grep "Socket(s):" | awk '{print $2}'`



# params from env params (tester.py for details)
llc_mask_scaling=$env_llc_mask_scaling
llc_assoc=$env_llc_assoc
core_freq_scaling=$env_core_freq_scaling
uncore_freq_scaling=$env_uncore_freq_scaling
memspeed=$env_memspeed
sku=$env_sku
cores_used=$env_cores_used
threads_used=$env_threads_used
smt=$env_smt
emon_starttime=$env_emon_starttime
emon_duration=$env_emon_duration
workload_name=$env_workload_name
working_directory=$env_working_directory
cmd=$env_cmd_list
numactl=$env_numactl_list


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

function wait_instances_end ()
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



data_folder=$(pwd)/data
mkdir -p $data_folder

declare -a cpu_freq_scaling_list=$core_freq_scaling
declare -a uncore_freq_scaling_list=$uncore_freq_scaling
declare -a llc_mask_scaling_list=$llc_mask_scaling

for freq_idx in "${!cpu_freq_scaling_list[@]}";
do
    freq=`echo ${cpu_freq_scaling_list[$freq_idx]}*1000000 | bc | awk '{printf "%d", $0}'`
    pushd ${setcpu_freq_dir}
    echo "[-------- Core Freq --------]"
    echo "./hwpdesire.sh -f $freq"
    ./hwpdesire.sh -f $freq
    popd

    for uncore_idx in "${!uncore_freq_scaling_list[@]}";
    do
        msr_val=`echo "ibase=10;obase=16; ${uncore_freq_scaling_list[$uncore_idx]}*10" | bc | awk '{printf "%d", $0}'`
        echo "[-------- Uncore Freq --------]"
        echo "wrmsr -a 0x620 0x${msr_val}${msr_val}"
        wrmsr -a 0x620 0x${msr_val}${msr_val}

        for llc_mask_idx in "${!llc_mask_scaling_list[@]}";
        do
            export PATH=${rdt_path}/pqos${PATH:+:${PATH}}
            export LD_LIBRARY_PATH=${rdt_path}/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
            echo "reset pqos: pqos -R"
            pqos -R
            mask="llc:1=${llc_mask_scaling_list[$llc_mask_idx]}"
            echo "[-------- LLC Mask --------]"
            echo "pqos -e $mask"
            pqos -e $mask
            assoc="core:1=${llc_assoc}"
            echo "pqos -a $assoc"
            pqos -a $assoc
            pqos -s > ${data_folder}/pqos_setting
            sleep 1

            # label of current case
            timets=$(date "+%Y%m%d%H%M")
            name="${workload_name}_${cores_per_socket}C${sockets}S_llc${llc_mask_scaling_list[$llc_mask_idx]}_${cores_used}C${threads_used}T_core${cpu_freq_scaling_list[$freq_idx]}_uncore${uncore_freq_scaling_list[$uncore_idx]}_mem${memspeed}_${sku}_${timets}"
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
                wait_instances_end "$cmd"
            elif [ $emon_duration -lt 0 ]; then
                # wait and then stop emon
                echo "[-------- emon: monitering the entire process. --------]"
                wait_instances_end "$cmd"
                bash ${emon_dir}/stop_emon.sh
            else
                # wait
                wait_instances_end "$cmd"
            fi


            echo $(pwd)
            if [ $emon_duration -gt 0 ] ; then
                mv *.log ${data_folder}/pqos_setting ${emon_dir}/${name}
            else
                mkdir -p ${emon_dir}/${name}
                mv *.log ${data_folder}/pqos_setting ${emon_dir}/${name}
            fi


            # custom content
            #mv jbb102/*jdk_specjbb2015* ${emon_dir}/${name}


            # data moving
            mv ${emon_dir}/${name} ${data_folder}

            # llc reset
            echo "reset pqos: pqos -R"
            pqos -R

        done
    done
done

exit 0
