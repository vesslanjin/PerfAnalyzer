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


# specjbb2015
pshell_content = "cat */result/*/*/*.raw | grep 'critical-jOPS' | cut -d '=' -f2 | sed -e 's/^[ ]*//'"


def walk_and_create_pshell(rdir):
    for root, dirs, files in os.walk(rdir):
        print(root)
        for name in dirs:
            pshell_path = os.path.join(root, name)
            # create pshell 'performance.sh'
            pshell = os.path.join(pshell_path, 'performance.sh')
            create_pshell(pshell)
        break


def create_pshell(pshell):
    swd = os.path.dirname(pshell)
    cwd = os.getcwd()
    filename = os.path.split(pshell)[-1]
    os.chdir(swd)
    cmd = 'echo "{0}" > {1}'.format(pshell_content,filename)
    print(cmd)
    subprocess.call(cmd, shell=True)
    os.chdir(cwd)



if __name__ == '__main__':
    walk_and_create_pshell('data')
