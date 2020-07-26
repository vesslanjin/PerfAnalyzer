Intel Sample Source Code License

Copyright(c) 2015-2020 Intel Corporation. All rights reserved.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the distribution.
    * Neither the name of Intel Corporation nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# 使用 jruby 版本的 emon process.sh （非常关键！）

## Jruby 版本

jprocess.sh
``` bash
#!/bin/bash
####################################################################################
# EDP script to post process emon data in linux, generates a bunch of csv's
# prerequisites:
#       Install oracle-java8-installer
#       sudo -E apt-get install ruby jruby
#       sudo -E jruby -S gem install jruby-win32ole <optional>
#####################################################################################

# cd $1

# Fix the path for EDP ruby script and processor specific EDP files
EDPRB=edp.rb
METRICS=zen2-rome.xml
CHART_FORMAT=chart_format_zen2.txt

# fix the path for the EMON input files
EMON_DATA=emon.dat
EMON_V=emon-v.dat
EMON_M=emon-M.dat
OUTPUT=summary.xlsx

CPUS=`grep -c ^processor /proc/cpuinfo`
THREADS=$(( CPUS * 3 / 4 ))
FreeMEM=`free -m | head -2 | tail -1 | awk '{ print $4 }'`
FreeMEM=$(( $FreeMEM - 1024 ))
echo Usable $THREADS threads with $FreeMEM MB memory.

JRUBY_OPTIONS="--server -J-Xmx${FreeMEM}m -J-Xms${FreeMEM}m --1.8"
PARALLELISM=$THREADS


BEGIN=1
END=1000000
QPI=6.4

#VIEW="--socket-view --thread-view"
VIEW="--socket-view --core-view --thread-view"
#VIEW=""

#TIMESTAMP_IN_CHART="--timestamp-in-chart"
TIMESTAMP_IN_CHART=""

echo Starting to parallel process the EDP data at `date +"%d-%b-%Y %r"`

#echo "jruby $JRUBY_OPTIONS $EDPRB -i $EMON_DATA -j $EMON_V -k $EMON_M -f $CHART_FORMAT -o $OUTPUT -m $METRICS -b $BEGIN -e $END -q $QPI $VIEW -p $PARALLELISM"
jruby $JRUBY_OPTIONS $EDPRB -i $EMON_DATA -j $EMON_V -k $EMON_M -f $CHART_FORMAT -o $OUTPUT -m $METRICS -b $BEGIN -e $END -q $QPI $VIEW -s 1 -p $PARALLELISM

echo Finished parallel processing the EDP data at `date +"%d-%b-%Y %r"`

exit
```

## ruby 版本

process.sh
``` bash
##ruby interpreter, change it according to the path where ruby is installed in your system
RUBY=ruby

##input file names, you may need to change them
EMON_DATA=emon.dat
EMON_V=emon-v.dat
EMON_M=emon-M.dat

##Workload related H/W and S/W configuration file; imported as-is into EDP spreadshe
CONFIG_FILE=config.xlsx

##Output of dmidecode; imported as-is into EDP spreadsheet
DMIDECODE_FILE=dmidecode.txt

##output of sar or other tool with network traffic
NETWORKSTAT_FILE=network.txt

##output of iostat or other tool with disk traffic
DISKSTAT_FILE=diskstat.txt

##output file name, you may want to change it

OUTPUT=summary.xlsx

##the metrics definition file; need to change this based on the architecture
METRICS=clx-2s.xml

##Excel chart format file, Need to change it based on the architecture
CHART_FORMAT=chart_format_clx_2s.txt

##the average value will be calculated from the %BEGIN% sample to %END% sample.
##setting %END% to a negative value means the last availabe sample.
BEGIN=1
END=1000000

VIEW="--socket-view --core-view --thread-view"

ruby edp.rb -i $EMON_DATA -j $EMON_V -k $EMON_M -g $CONFIG_FILE -d $DMIDECODE_FILE -D $DISKSTAT_FILE -n $NETWORKSTAT_FILE -f $CHART_FORMAT -o $OUTPUT -m $METRICS -b $BEGIN -e $END $VIEW $TPS $TIMESTAMP_IN_CHART

exit
```

# Jruby 安装

* https://www.jruby.org/download
``` bash
$ wget https://repo1.maven.org/maven2/org/jruby/jruby-dist/9.2.11.1/jruby-dist-9.2.11.1-bin.tar.gz
$ tar -zxvf jruby-dist-9.2.11.1-bin.tar.gz
$ export JRUBY_HOME=/home/tools/jruby-9.2.11.1${JRUBY_HOME:+:${JRUBY_HOME}}
$ export PATH=/home/tools/jruby-9.2.11.1/bin${PATH:+:${PATH}}
```

``` bash
$ jruby -v
```
