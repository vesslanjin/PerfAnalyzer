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
from dao import Config, Cpi, Emon
from popo import CpiDetails
from config_service import config_ids_spliting
from sku_service import load_skus

import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


def build_cpi_model(config_ids):
    if len(config_ids) < 1:
        return {"ccpi": None, "bf": None}
    # redo cpi model
    emons = Emon.query.filter(Emon.config_id.in_(config_ids)).all()
    mpi_x_mp_list = []
    cpi_list = []
    for emon in emons:
        mpi_x_mp = emon.llc_mpi * emon.llc_mpns * emon.cpu_freq
        cpi = emon.cpi
        mpi_x_mp_list.append(mpi_x_mp)
        cpi_list.append(cpi)
    reg = linear_model.LinearRegression()
    reg.fit(np.array(mpi_x_mp_list).reshape(-1, 1), cpi_list)
    ccpi = reg.intercept_                                                          #cpi cache
    bf = reg.coef_[0]                                                              #bf
    return {"ccpi": ccpi, "bf": bf}

def build_tb_cpi(config_ids):
    if len(config_ids) < 1:
        return
    # redo cpi model
    emons = Emon.query.filter(Emon.config_id.in_(config_ids)).all()
    mpi_x_mp_list = []
    cpi_list = []
    for emon in emons:
        mpi_x_mp = emon.llc_mpi * emon.llc_mpns * emon.cpu_freq
        cpi = emon.cpi
        mpi_x_mp_list.append(mpi_x_mp)
        cpi_list.append(cpi)
    reg = linear_model.LinearRegression()
    reg.fit(np.array(mpi_x_mp_list).reshape(-1, 1), cpi_list)
    ccpi = reg.intercept_                                                          #cpi cache
    bf = reg.coef_[0]                                                              #bf
    # clear tb_cpi
    for cpi in Cpi.query.all():
        db_session.delete(cpi)
    db_session.commit()
    # build tb_cpi
    for emon in emons:
        cpi = Cpi()
        cpi.emon_id = emon.id
        cpi.mpi_x_mp = emon.llc_mpi * emon.llc_mpns * emon.cpu_freq
        cpi.cpi = emon.cpi
        cpi.ccpi = ccpi
        cpi.bf = bf
        computed_cpi = cpi.ccpi + cpi.mpi_x_mp * cpi.bf
        lgroups = emon.label.upper().split('_')
        cores_per_skt = int(lgroups[1].split('C')[0])
        cores = int(lgroups[3].split('C')[0])
        threads = int(lgroups[3].split('C')[-1].split('T')[0])
        single_cpu_util = emon.cpu_util * cores_per_skt / cores
        cpi.error_rate = (computed_cpi - cpi.cpi)/cpi.cpi
        cpi.mips = (single_cpu_util/100) * 1000 * emon.cpu_freq * threads / cpi.cpi
        db_session.add(cpi)
    db_session.commit()

def cpi_details_list(config_ids):
    """
    Please make sure you have exec 'build_tb_cpi'.
    """
    cpi_details_list = []
    emons = Emon.query.filter(Emon.config_id.in_(config_ids)).all()
    for emon in emons:
        emon_id = emon.id
        config_id = emon.config_id
        # config info, cpi info, label info
        config = Config.query.filter(Config.id == config_id).first()
        cpi = Cpi.query.filter(Cpi.emon_id == emon_id).first()
        lgroups = emon.label.upper().split('_')
        # CpiDetails
        cpiDetails = CpiDetails()
        cpiDetails.workload = config.workload
        cpiDetails.sku = config.sku
        cpiDetails.cores = config.cores
        cpiDetails.threads = float(config.cores)*float(config.smt)
        cores_per_socket = int(lgroups[1].split('C')[0])
        cpiDetails.cores_per_socket = cores_per_socket
        cpiDetails.llc = maskbits(config.llc) * cores_per_socket * 1.375 / 11         # Hint! max llc mask is 0x7FF   
        cpiDetails.memory_speed = emon.mem_speed
        cpiDetails.core_frequency = emon.cpu_freq
        cpiDetails.uncore_frequency = emon.uncore_freq
        cpiDetails.cpi = emon.cpi
        cpiDetails.computed_cpi = cpi.ccpi + cpi.mpi_x_mp * cpi.bf
        cpiDetails.cpi_error_rate = (cpiDetails.computed_cpi - cpi.cpi)/cpi.cpi
        single_cpu_util = emon.cpu_util * cores_per_socket / float(config.cores)
        cpiDetails.cpu_util = single_cpu_util
        cpiDetails.mips = (single_cpu_util/100) * 1000 * cpiDetails.core_frequency * cpiDetails.threads / cpiDetails.cpi
        cpiDetails.performance = emon.performance
        # append
        cpi_details_list.append(cpiDetails)
    return cpi_details_list

def maskbits(s):
    val = None
    try:
        val = int(s, 16)
    except ValueError:
        raise argparse.ArgumentError("Bad hex number %s" % (s))
    return bin(val).count('1')


def core_frequency_scaling(legends_dic):
    series = []
    for legend,config_ids in legends_dic.items():
        if len(config_ids) < 2:
            continue
        emons = Emon.query.filter(Emon.config_id.in_(config_ids)).all()
        data = []
        for emon in emons:
            cpi = Cpi.query.filter(Cpi.emon_id == emon.id).first()
            core_frequency = emon.cpu_freq
            performance = emon.performance if emon.performance is not None else cpi.mips
            data.append((core_frequency, performance))
        points, label, degree = polynomial_regression(data)
        series.append({"data": data, "points": points, "label": label, "legend": legend, "degree": degree})
    return series

def core_num_scaling(legends_dic):
    series = []
    for legend,config_ids in legends_dic.items():
        if len(config_ids) < 2:
            continue
        configs = Config.query.filter(Config.id.in_(config_ids)).all()
        data = []
        for config in configs:
            emon = Emon.query.filter(Emon.config_id == config.id).first()
            cpi = Cpi.query.filter(Cpi.emon_id == emon.id).first()
            core_num = config.cores
            performance = emon.performance if emon.performance is not None else cpi.mips
            data.append((core_num, performance))
        points, label, degree = polynomial_regression(data)
        series.append({"data": data, "points": points, "label": label, "legend": legend, "degree": degree})
    return series

def uncore_frequency_scaling(legends_dic):
    series = []
    for legend,config_ids in legends_dic.items():
        if len(config_ids) < 2:
            continue
        emons = Emon.query.filter(Emon.config_id.in_(config_ids)).all()
        data = []
        for emon in emons:
            cpi = Cpi.query.filter(Cpi.emon_id == emon.id).first()
            uncore_frequency = emon.uncore_freq
            performance = emon.performance if emon.performance is not None else cpi.mips
            data.append((uncore_frequency, performance))
        points, label, degree = polynomial_regression(data)
        series.append({"data": data, "points": points, "label": label, "legend": legend, "degree": degree})
    return series

def llc_mb_scaling(legends_dic):
    series = []
    for legend,config_ids in legends_dic.items():
        if len(config_ids) < 2:
            continue
        configs = Config.query.filter(Config.id.in_(config_ids)).all()
        data = []
        for config in configs:
            emon = Emon.query.filter(Emon.config_id == config.id).first()
            cpi = Cpi.query.filter(Cpi.emon_id == emon.id).first()
            lgroups = emon.label.upper().split('_')
            cores_per_socket = float(lgroups[1].split('C')[0])
            llc_mb = maskbits(config.llc) * cores_per_socket * 1.375 / 11         # Hint! max llc mask is 0x7FF
            performance = emon.performance if emon.performance is not None else cpi.mips
            data.append((llc_mb, performance))
        points, label, degree = polynomial_regression(data)
        series.append({"data": data, "points": points, "label": label, "legend": legend, "degree": degree})
    return series

def polynomial_regression(data):
    points = []
    label = ''
    degree = 1
    if len(data) < 2:
        points = data
        label = ''
        degree = 0
        return points, label, degree
    data = np.array(data, dtype=np.float32)
    xdata = data[:,0][:, np.newaxis]
    rdata = data[:,1]
    # do regression
    _, xtransformed = transfrom(xdata, degree)                #索引多维数组的某一列时，返回的仍然是列的结构
    reg = linear_model.LinearRegression()
    reg.fit(xtransformed, rdata)
    coef = reg.coef_
    intercept = reg.intercept_
    label = 'y = {}x + {}'.format(coef[0], intercept)
    # smooth points
    ydata = np.dot(xtransformed, coef) + intercept
    points = np.hstack((xdata, ydata[:,np.newaxis]))
    points = points.tolist()
    points.sort(reverse=False, key=lambda elem: elem[0])
    return points, label, degree

def transfrom(X, degree):
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    xtransformed = poly.fit_transform(X)
    powers = poly.powers_
    return powers, xtransformed


def performance_modeling_glm(config_ids):
    options = {}
    # polynomial regression
    legends_dic = config_ids_spliting(config_ids, member='core_frequency')
    series = core_frequency_scaling(legends_dic)
    options['core_frequency'] = series[0]['degree'] if len(series) > 0 else 0
    legends_dic = config_ids_spliting(config_ids, member='cores')
    series = core_num_scaling(legends_dic)
    options['cores'] = series[0]['degree'] if len(series) > 0 else 0
    legends_dic = config_ids_spliting(config_ids, member='uncore_frequency')
    series = uncore_frequency_scaling(legends_dic)
    options['uncore_frequency'] = series[0]['degree'] if len(series) > 0 else 0
    legends_dic = config_ids_spliting(config_ids, member='llc')
    series = llc_mb_scaling(legends_dic)
    options['llc'] = series[0]['degree'] if len(series) > 0 else 0
    # get cpi details list for glm
    details_list = cpi_details_list(config_ids)
    # glm
    result = cpi_details_glm_modling(details_list, options)
    return result

def cpi_details_glm_modling(details_list, options={'core_frequency' : 1, 'cores' : 1, 'uncore_frequency' : 1, 'llc' : 1}):
    keys = ['core_frequency', 'cores', 'uncore_frequency', 'llc']
    xdata = []
    ydata = []
    for detail in details_list:
        xdata.append((detail.core_frequency, detail.cores, detail.uncore_frequency, detail.llc))
        performance = detail.performance if detail.performance is not None else detail.mips
        ydata.append(performance)
    validdata = glm_input_data_preprocess(xdata, keys, options)
    # 特别注意：病态矩阵求解问题。。
    reg = linear_model.Ridge(alpha=0.5)
    reg.fit(validdata, ydata)
    coef = reg.coef_
    intercept = reg.intercept_
    # update evaluation error rate
    evals = np.dot(validdata, coef) + intercept
    for idx, detail in enumerate(details_list):
        ground_truth = ydata[idx]
        evaluation = evals[idx]
        eval_error_rate = (evaluation-ground_truth)/ground_truth
        details_list[idx].evaluation = evaluation
        details_list[idx].eval_error_rate = eval_error_rate
    # cpi_details_list with evaluation info
    return {'details_list': details_list, 'keys': keys, 'options': options, 'coef': coef.tolist(), 'intercept': float(intercept)}

def glm_input_data_preprocess(data, keys, options):
    maxdeg = 0
    for key in keys:
        deg = options[key] if key in options else 0
        maxdeg = maxdeg + deg
    # data pre-process
    xdata = np.array(data, dtype=np.float32)
    powers, tdxdata = transfrom(xdata, maxdeg)
    validdata = None
    for i, power in enumerate(powers):
        passcol = False
        for j, p in enumerate(power):
            limval = options[keys[j]] if keys[j] in options else 0
            if p > limval:
                passcol = True
                break
        if passcol is True:
            continue
        # find a valid column
        col = tdxdata[:, i][...,np.newaxis]
        if validdata is None:
            validdata = col
        else:
            validdata = np.hstack((validdata, col))
    # final input data is: validdata
    return validdata


def performance_evaluation_glm(data):
    cpu_struc = data['cpuStruc']
    current_sku = data['sku']
    keys = data['keys']
    options = data['options']
    coef = data['coef']
    intercept= data['intercept']
    # load skus
    skus = load_skus(cpu_struc)
    # base performance
    xdata = []
    for sku in skus:
        #keys = ['core_frequency', 'cores', 'uncore_frequency', 'llc']
        rowdata = []
        for key in keys:
            if 'core_frequency' == key:
                rowdata.append(sku.base_core_frequency)
            if 'cores' == key:
                rowdata.append(sku.cores)
            if 'uncore_frequency' == key:
                rowdata.append(sku.uncore_frequency)
            if 'llc' == key:
                rowdata.append(sku.llc_mb)
        xdata.append(rowdata)
    basedata = glm_input_data_preprocess(xdata, keys, options)
    # turbo performance
    xdata = []
    for sku in skus:
        #keys = ['core_frequency', 'cores', 'uncore_frequency', 'llc']
        rowdata = []
        for key in keys:
            if 'core_frequency' == key:
                rowdata.append(sku.turbo_core_frequency)
            if 'cores' == key:
                rowdata.append(sku.cores)
            if 'uncore_frequency' == key:
                rowdata.append(sku.uncore_frequency)
            if 'llc' == key:
                rowdata.append(sku.llc_mb)
        xdata.append(rowdata)
    turbodata = glm_input_data_preprocess(xdata, keys, options)
    base_performances = np.dot(basedata, coef) + intercept
    turbo_performances = np.dot(turbodata, coef) + intercept
    # update skus info
    for i, sku in enumerate(skus):
        skus[i].base_performance = base_performances[i]
        skus[i].turbo_performance = turbo_performances[i]
    return skus



if __name__ == "__main__":
    config_ids = [1,2]
    cpi_model = build_cpi_model(config_ids)
    print(cpi_model)
    print(maskbits('0x3f'))
    cpi_details_list = cpi_details_list(config_ids)
    print(cpi_details_list)
