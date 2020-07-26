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

from dao import init_db, db_session
from dao import Config, Emon


def get_settings():
    settings = {}
    settings["workload"] = [config.workload for config in Config.query.group_by(Config.workload)]
    settings["sku"] = [config.sku for config in Config.query.group_by(Config.sku)]
    settings["smt"] = [config.smt for config in Config.query.group_by(Config.smt)]
    settings["memory_speed"] = [config.memory_speed for config in Config.query.group_by(Config.memory_speed)]
    settings["llc"] = [config.llc for config in Config.query.group_by(Config.llc)]
    settings["cores"] = [config.cores for config in Config.query.group_by(Config.cores)]
    settings["core_frequency"] = [config.core_frequency for config in Config.query.group_by(Config.core_frequency)]
    settings["uncore_frequency"] = [config.uncore_frequency for config in Config.query.group_by(Config.uncore_frequency)]
    for k, v in settings.items():
        v.insert(0, "All")
    return settings

def get_settings_without_all_option():
    settings = {}
    settings["workload"] = [config.workload for config in Config.query.group_by(Config.workload)]
    settings["sku"] = [config.sku for config in Config.query.group_by(Config.sku)]
    settings["smt"] = [config.smt for config in Config.query.group_by(Config.smt)]
    settings["memory_speed"] = [config.memory_speed for config in Config.query.group_by(Config.memory_speed)]
    settings["llc"] = [config.llc for config in Config.query.group_by(Config.llc)]
    settings["cores"] = [config.cores for config in Config.query.group_by(Config.cores)]
    settings["core_frequency"] = [config.core_frequency for config in Config.query.group_by(Config.core_frequency)]
    settings["uncore_frequency"] = [config.uncore_frequency for config in Config.query.group_by(Config.uncore_frequency)]
    return settings

def get_config_ids(setting):
    options = parse_selected_options(setting)
    config_ids = [config.id for config in Config.query.filter(
        Config.workload.in_(options['workload'])).filter(
        Config.sku.in_(options['sku'])).filter(
        Config.smt.in_(options['smt'])).filter(
        Config.memory_speed.in_(options['memory_speed'])).filter(
        Config.llc.in_(options['llc'])).filter(
        Config.cores.in_(options['cores'])).filter(
        Config.core_frequency.in_(options['core_frequency'])).filter(
        Config.uncore_frequency.in_(options['uncore_frequency'])).all()
        ]
    return config_ids

def parse_selected_options(setting):
    options = get_settings_without_all_option()
    for k, v in setting.items():
        if "All" in setting[k]:
            pass
        else:
            if (isinstance(setting[k], str)):
                options[k] = [ setting[k], ]
            else:
                options[k] = setting[k]
    return options

def config_ids_spliting(config_ids, member=''):
    items = ['cores', 'memory_speed', 'sku', 'core_frequency', 'llc', 'smt', 'workload', 'uncore_frequency']
    legends_dic = {}
    for config_id in config_ids:
        emon = Emon.query.filter(Emon.config_id == config_id).all()
        if len(emon) < 1:
            continue
        config = Config.query.filter(Config.id == config_id).first()
        legend = '-'
        for name, value in vars(config).items():
            if member == name:
                continue
            if name in items:
                legend = legend + '{}{}-'.format(name,value)
        if legend in legends_dic:
            legends_dic[legend].append(config_id)
        else:
            legends_dic[legend] = [config_id,]
    return legends_dic


# Unit Tests
if __name__ == "__main__":
    settings =  get_settings()
    print(settings)
