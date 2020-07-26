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
import os
import sys
import subprocess
from multiprocessing import Process


def walk_and_run_process(rdir):
    for root, dirs, files in os.walk(rdir):
        print(root)
        for name in dirs:
            emon_data_path = os.path.join(root, name)
            # run process
            pshell = os.path.join(emon_data_path, 'process.sh')
            run_pshell(pshell)                                        #请使用JRuby版本的EDP！
            #newprocess(target=run_pshell, args=(pshell,))
        break                                                         #stop down to next level


def run_pshell(pshell):
    swd = os.path.dirname(pshell)
    cwd = os.getcwd()
    filename = os.path.split(pshell)[-1]
    os.chdir(swd)
    if os.path.exists("__edp_socket_view_summary.csv"):
        return  # pass if csv existed
    print(pshell)
    result = subprocess.getoutput('bash {}'.format(filename))          #Python3
    #subprocess.call('bash {}'.format(filename), shell=True)           #Python2
    print(result)
    os.chdir(cwd)


def newprocess(target, args):
    p = Process(target=target, args=args)
    p.start()



if __name__ == '__main__':
    walk_and_run_process('data')
