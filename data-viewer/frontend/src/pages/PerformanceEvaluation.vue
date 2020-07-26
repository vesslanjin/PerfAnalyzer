<template>
  <v-card outlined tile class="mt-3">
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-responsive :aspect-ratio="4/1">
            <div ref="performanceEvaluationChart" style="width:100%;height:100%;"></div>
          </v-responsive>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
// See https://www.echartsjs.com/examples/en/editor.html?c=bar1
// See https://www.echartsjs.com/examples/en/editor.html?c=bar-label-rotation
import echarts from 'echarts'

export default {
    data: () => ({
        cpuStruc: 'Skylake',
    }),
    computed: {
        performanceModelingGlm: function () {
            return this.$root.$data.sharedState.performanceModelingGlm;
        },
        config: function () {
            return this.$root.$data.sharedState.config;
      },
    },
    watch: {
        performanceModelingGlm: {
            deep: true,
            handler: function (val, oldVal) {
                this.performance_evaluation_glm();
            }
        },
    },
    methods: {
        performance_evaluation_glm () {
            let data = {
                cpuStruc: this.cpuStruc,
                sku: this.config.sku,
                keys: this.performanceModelingGlm.keys,
                options: this.performanceModelingGlm.options,
                coef: this.performanceModelingGlm.coef,
                intercept: this.performanceModelingGlm.intercept
            };
            this.$http.post('/performance/evaluation/glm', data).then(resp => {
                let data = resp.data.map(o => JSON.parse(o));
                let subtitle = this.config.workload + ' on ' + this.cpuStruc;
                let {legends, xAxisData, series} = this.parseData(data);
                this.drawEvaluationChart(this.$refs.performanceEvaluationChart, 'Performancde Evaluation', subtitle, legends, xAxisData, series);
            }).catch(() => {
            });
        },
        parseData (data) {
            let legends = ['base', 'turbo'];
            let xAxisData = [];
            let series = [
                    {
                        name: 'base',
                        type: 'bar',
                        data: [],
                        markPoint: {
                            data: [
                                {type: 'max', name: '最大值'},
                                {type: 'min', name: '最小值'}
                            ]
                        },
                        markLine: {
                            data: [
                                {type: 'average', name: '平均值'}
                            ],
                            lineStyle: { color: 'transparent' },
                        }
                    },
                    {
                        name: 'turbo',
                        type: 'bar',
                        data: [],
                        markPoint: {
                            data: [
                                {type: 'max', name: '最大值'},
                                {type: 'min', name: '最小值'}
                            ]
                        },
                        markLine: {
                            data: [
                                {type: 'average', name: '平均值'}
                            ],
                            lineStyle: { color: 'transparent' },
                        }
                    }
                ];
            data.forEach(o => {
                let base_performance = parseFloat(o.base_performance).toFixed(2);
                let turbo_performance = parseFloat(o.turbo_performance).toFixed(2);
                if (base_performance < 0 || turbo_performance < 0) {
                    return;  //过滤掉有误数据。
                }
                xAxisData.push(o.name);
                series[0].data.push(base_performance);
                series[1].data.push(turbo_performance);
            });
            return { legends: legends, xAxisData: xAxisData, series: series};
        },
        drawEvaluationChart (dom, title, subtitle, legends, xAxisData, series) {
            dom.removeAttribute("_echarts_instance_");
            let myChart = echarts.init(dom);
            let option = {
                title: {
                    text: title,
                    subtext: subtitle
                },
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    data: legends
                },
                toolbox: {
                    show: true,
                    feature: {
                        dataView: {show: true, readOnly: false},
                        magicType: {show: false, type: ['line', 'bar']},
                        restore: {show: false},
                        saveAsImage: {show: true}
                    }
                },
                calculable: true,
                xAxis: [
                    {
                        type: 'category',
                        data: xAxisData
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: series
            };
            myChart.setOption(option);
            window.addEventListener("resize", () => { myChart.resize(); });
        },
    },
}
</script>

<style scoped>
</style>