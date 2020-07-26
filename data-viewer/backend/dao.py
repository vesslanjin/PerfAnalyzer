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

from sqlalchemy import create_engine, MetaData, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import mapper, relationship

engine = create_engine('sqlite:///data.db', convert_unicode=True, connect_args={'check_same_thread':False})
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
#session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    metadata.create_all(bind=engine)


# Tables
config = Table('tb_config', metadata,
               Column('id', Integer, primary_key=True, autoincrement=True),
               Column('workload', String(64)),
               Column('sku', String(64)),
               Column('smt', String(64)),
               Column('memory_speed', String(64)),
               Column('llc', String(64)),
               Column('cores', String(64)),
               Column('core_frequency', String(64)),
               Column('uncore_frequency', String(64))
               )

emon = Table('tb_emon', metadata,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('config_id', Integer),
             Column('label', Text),
             Column('socket', String(64)),
             Column('mem_speed', Float),
             Column('cpu_freq', Float),
             Column('uncore_freq', Float),
             Column('cpu_util', Float),
             Column('llc_mpi', Float),
             Column('llc_mpns', Float),
             Column('cpi', Float),
             Column('performance', Float)
             )

cpi = Table('tb_cpi', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('emon_id', Integer),
            Column('mpi_x_mp', Float),
            Column('ccpi', Float),
            Column('bf', Float),
            Column('cpi', Float),
            Column('error_rate', Float),
            Column('mips', Float)
            )


# Objects
class Config(object):
    query = db_session.query_property()

    def __init__(self, id=None,
                 workload=None,
                 sku=None,
                 smt=None,
                 memory_speed=None,
                 llc=None,
                 cores=None,
                 core_frequency=None,
                 uncore_frequency=None):
        self.id = id
        self.workload = workload
        self.sku = sku
        self.smt = smt
        self.memory_speed = memory_speed
        self.llc = llc
        self.cores = cores
        self.core_frequency = core_frequency
        self.uncore_frequency = uncore_frequency

    def __repr__(self):
        return '<Config id=%r workload=%r sku=%r>' % (self.id, self.workload, self.sku)


class Emon(object):
    query = db_session.query_property()

    def __init__(self, id=None,
                 config_id=None,
                 label=None,
                 socket=None,
                 mem_speed=None,
                 cpu_freq=None,
                 uncore_freq=None,
                 cpu_util=None,
                 llc_mpi=None,
                 llc_mpns=None,
                 cpi=None,
                 performance=None):
        self.id = id
        self.config_id = config_id
        self.label = label
        self.socket = socket
        self.mem_speed = mem_speed
        self.cpu_freq = cpu_freq
        self.uncore_freq = uncore_freq
        self.cpu_util = cpu_util
        self.llc_mpi = llc_mpi
        self.llc_mpns = llc_mpns
        self.cpi = cpi
        self.performance = performance

    def __repr__(self):
        return '<Emon id=%r config_id=%r label=%r socket=%r>' % (self.id, self.config_id, self.label, self.socket)


class Cpi(object):
    query = db_session.query_property()

    def __init__(self, id=None,
                 emon_id=None,
                 mpi_x_mp=None,
                 ccpi=None,
                 bf=None,
                 cpi=None,
                 error_rate=None,
                 mips=None):
        self.id = id
        self.emon_id = emon_id
        self.mpi_x_mp = mpi_x_mp
        self.ccpi = ccpi
        self.bf = bf
        self.cpi = cpi
        self.error_rate = error_rate
        self.mips = mips

    def __repr__(self):
        return '<Cpi id=%r emon_id=%r mpi_x_mp=%r cpi=%r>' % (self.id, self.emon_id, self.mpi_x_mp, self.cpi)


# ORM (Object Relational Mapping)
mapper(Config, config)
mapper(Emon, emon)
mapper(Cpi, cpi)

# main
if __name__ == '__main__':
    init_db()
