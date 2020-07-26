<template>
  <v-card outlined tile class="mt-3">
    <v-container>
      <v-row>
        <v-col cols="12" sm="6">
          <v-responsive :aspect-ratio="4/3">
            <div ref="coreFreqScalingChart" style="width:100%;height:100%;"></div>
          </v-responsive>
        </v-col>
        <v-col cols="12" sm="6">
          <v-responsive :aspect-ratio="4/3">
            <div ref="coreNumberScalingChart" style="width:100%;height:100%;"></div>
          </v-responsive>
        </v-col>
        <v-col cols="12" sm="6">
          <v-responsive :aspect-ratio="4/3">
            <div ref="uncoreFreqScalingChart" style="width:100%;height:100%;"></div>
          </v-responsive>
        </v-col>
        <v-col cols="12" sm="6">
          <v-responsive :aspect-ratio="4/3">
            <div ref="llcScalingChart" style="width:100%;height:100%;"></div>
          </v-responsive>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
// See https://echarts.apache.org/examples/en/editor.html?c=scatter-polynomial-regression
// Style https://www.runoob.com/echarts/echarts-style.html
import echarts from 'echarts'
import ecStat from 'echarts-stat'

export default {
    data: () => ({
        mockData: [{
            data: [
                [96.24, 11.35],
                [33.09, 85.11],
                [57.60, 36.61],
            ],
            points: [                                                           //Hint!! points must be sorted!
                [33.09, 85.11],
                [57.6, 36.61],
                [96.24, 11.35],
            ],
            label: 'y = f(x)',
        }]
    }),
    computed: {
        config: function () {
            return this.$root.$data.sharedState.config;
        },
        cpiDetailsListChanged: function () {
            return this.$root.$data.sharedState.cpiDetailsListChanged;
        },
    },
    watch: {
        cpiDetailsListChanged: {
            deep: true,
            handler: function (val, oldVal) {
                this.update_scaling_chart_corefreq();
                this.update_scaling_chart_corenum();
                this.update_scaling_chart_uncorefreq();
                this.update_scaling_chart_llc();
            }
        }
    },
    methods: {
        update_scaling_chart_corefreq () {
            this.$http.post('/cpi/scaling/corefreq', this.config).then(resp => {
                    let series = this.parseData(resp.data);
                    this.drawPolyRegChart(this.$refs.coreFreqScalingChart, series, 'Core Frequency Scaling Analysis', 'Performance', 'GHz');
            }).catch(() => {
            });
        },
        update_scaling_chart_corenum () {
            this.$http.post('/cpi/scaling/corenum', this.config).then(resp => {
                    let series = this.parseData(resp.data);
                    this.drawPolyRegChart(this.$refs.coreNumberScalingChart, series, 'Core Number Scaling Analysis', 'Performance', 'Core Number');
            }).catch(() => {
            });
        },
        update_scaling_chart_uncorefreq () {
            this.$http.post('/cpi/scaling/uncorefreq', this.config).then(resp => {
                    let series = this.parseData(resp.data);
                    this.drawPolyRegChart(this.$refs.uncoreFreqScalingChart, series, 'UnCore Frequency Scaling Analysis', 'Performance', 'GHz');
            }).catch(() => {
            });
        },
        update_scaling_chart_llc () {
            this.$http.post('/cpi/scaling/llc', this.config).then(resp => {
                    let series = this.parseData(resp.data);
                    this.drawPolyRegChart(this.$refs.llcScalingChart, series, 'Last Level Cache Scaling Analysis', 'Performance', 'MB');
            }).catch(() => {
            });
        },
        parseData (data) {
            let series = [];
            data.forEach(item => {
                //formatter
                this.dataFormat(item.data);
                this.dataFormat(item.points);
                //parse
                series.push({
                    type: 'scatter',
                    emphasis: {
                        label: {
                            show: true,
                            position: 'right',
                            fontSize: 16
                        }
                    },
                    data: item.data,
                });
                series.push({
                    type: 'line',
                    lineStyle: {
                        opacity: 0.25,
                        type: 'solid',
                    },
                    smooth: true,
                    showSymbol: false,
                    data: item.points,
                    markPoint: {
                        itemStyle: {
                            color: 'transparent'                                           //透明
                        },
                        label: {
                            show: true,
                            position: 'left',
                            formatter: item.label,
                            color: 'transparent',                                          //#333
                            fontSize: 14
                        },
                        data: [{
                            coord: item.points[item.points.length - 1]
                        }]
                    }
                });
            });
            return series;
        },
        dataFormat (points) {
            points.forEach(point => {
                point[0] = parseFloat(point[0]).toFixed(2);
                point[1] = parseFloat(point[1]).toFixed(2);
            });
        },
        drawPolyRegChart (dom, series, title, yAxisName, xAxisName) {
            dom.removeAttribute("_echarts_instance_");
            let myChart = echarts.init(dom);
            let option = {
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'cross'
                    },
                },
                title: {
                    text: title,
                    subtext: 'By polynomial regression',
                    left: 'center',
                    top: 3
                },
                xAxis: {
                    type: 'value',
                    name: xAxisName,
                },
                yAxis: {
                    type: 'value',
                    name: yAxisName,
                },
                grid: {
                    top: 80
                },
                series: series,
            };
            myChart.setOption(option);
            window.addEventListener("resize", () => { myChart.resize(); });
        },
    },
    created: function () {
        this.$nextTick(() => {
            let series = this.parseData(this.mockData);
            this.drawPolyRegChart(this.$refs.coreFreqScalingChart, series, 'Example: scatter-polynomial-regression', 'Performance', 'GHz');
            this.drawPolyRegChart(this.$refs.coreNumberScalingChart, series, 'Example: scatter-polynomial-regression', 'Performance', 'Core Number');
            this.drawPolyRegChart(this.$refs.uncoreFreqScalingChart, series, 'Example: scatter-polynomial-regression', 'Performance', 'GHz');
            this.drawPolyRegChart(this.$refs.llcScalingChart, series, 'Example: scatter-polynomial-regression', 'Performance', 'MB');
        });
    },
}
</script>

<style scoped>
</style>
