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

import os, json
from popo import Sku

STRUCTURE_MAPPER = {'Skylake': 'skx.json', 'CascadeLake': 'clx.json', 'Icelake': '', 'Broadwell': ''}


def load_skus(cpu_struc):
    filename = STRUCTURE_MAPPER[cpu_struc]
    jsonfile = os.path.join('skus', filename)
    skus = []
    if not os.path.exists(jsonfile):
        return skus
    with open(jsonfile, 'r') as f:
        data = json.load(f)
        items = data['data']
        for item in items:
            sku = Sku()
            sku.name = item['SKU']
            sku.cores = item['Cores']
            sku.uncore_frequency = item['CLMmax (GHz)']
            sku.llc_mb = item['LLC (MB)']
            sku.turbo_core_frequency = item['turbo_ratio'][str(item['Cores'])]
            sku.base_core_frequency = item['Base non-AVX Core Frequency (GHz)']
            sku.tdp = item['TDP (W)']
            skus.append(sku)
    return skus


if __name__ == '__main__':
    skus = load_skus('Skylake')
    print(skus)
