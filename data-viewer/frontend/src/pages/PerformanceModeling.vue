<template>
  <v-card outlined tile class="mt-3">
    <v-data-table outlined tile
      :headers="headers"
      :items="dataSet"
      :items-per-page="5"
      :sort-by="[]"
      :sort-desc="[]"
      :page.sync="page"
      class="elevation-1"
    >
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  data: () => ({
      headers: [
          {text: 'SKU', value: 'SKU', align: 'start', sortable: false},
          {text: 'CORES', value: 'CORES', align: 'center', sortable: false},
          {text: 'THREADS', value: 'THREADS', align: 'center', sortable: false},
          {text: 'LLC_SIZE', value: 'LLC_SIZE', align: 'center', sortable: false},
          {text: 'MEM_SPEED', value: 'MEM_SPEED', align: 'center', sortable: false},
          {text: 'CORE_FREQ', value: 'CORE_FREQ', align: 'center', sortable: false},
          {text: 'UNCORE_FREQ', value: 'UNCORE_FREQ', align: 'center', sortable: false},
          {text: 'CPI', value: 'CPI', align: 'center', sortable: false},
          {text: 'COMPUTED_CPI', value: 'COMPUTED_CPI', align: 'center', sortable: false},
          {text: 'CPI_ERR', value: 'CPI_ERR', align: 'center', sortable: false},
          {text: 'CPU_UTIL', value: 'CPU_UTIL', align: 'center', sortable: false},
          {text: 'MIPS', value: 'MIPS', align: 'center', sortable: false},
          {text: 'PERFORMANCE', value: 'PERFORMANCE', align: 'center', sortable: false},
          {text: 'EVAL', value: 'EVALUATION', align: 'center', sortable: false},
          {text: 'EVAL_ERR', value: 'EVAL_ERR_RATE', align: 'center', sortable: false},
          {text: 'CORES_PER_SOCKET', value: 'CORES_PER_SOCKET', align: 'center', sortable: false},
      ],
      dataSet: [],
      page: 1,
  }),
  computed: {
      config: function () {
          let { workload, sku, smt, memory_speed, llc, uncore_frequency, ...others} = this.$root.$data.sharedState.config;
          let config = {
              workload: workload,
              sku: sku,
              smt: smt,
              memory_speed: memory_speed,
              llc: llc,
              uncore_frequency: uncore_frequency,
              cores: 'All',
              core_frequency: 'All',
          };
          return config;
      },
      cpiDetailsListChanged: function () {
          return this.$root.$data.sharedState.cpiDetailsListChanged;
      },
  },
  watch: {
      cpiDetailsListChanged: {
          deep: true,
          handler: function (val, oldVal) {
              this.performance_modeling_glm();
          }
      },
  },
  methods: {
    performance_modeling_glm () {
        this.$http.post('/performance/modeling/glm', this.config).then(resp => {
            let data = resp.data;
            this.dataSet = data.details_list.map(o => JSON.parse(o));
            console.log(data.options);
            //formatter
            this.dataFormat(this.dataSet);
            this.page = 1;
            let flash = !this.$root.$data.sharedState.performanceModelingGlm.flash;
            this.$root.$data.sharedState.performanceModelingGlm = {
                flash: flash,
                keys: data.keys,
                options: data.options,
                coef: data.coef,
                intercept: data.intercept
            };
        }).catch(() => {
        });
    },
    dataFormat (data) {
        data.forEach(item => {
            item.CORES = parseInt(item.CORES);
            item.THREADS = parseInt(item.THREADS);
            item.LLC_SIZE = parseFloat(item.LLC_SIZE).toFixed(1);
            item.MEM_SPEED = parseInt(item.MEM_SPEED);
            item.CORE_FREQ = parseFloat(item.CORE_FREQ).toFixed(1);
            item.UNCORE_FREQ = parseFloat(item.UNCORE_FREQ).toFixed(1);
            item.CPI = parseFloat(item.CPI).toFixed(2);
            item.COMPUTED_CPI = parseFloat(item.COMPUTED_CPI).toFixed(2);
            item.CPI_ERR = (parseFloat(item.CPI_ERR) * 100).toFixed(2) + '%';
            item.CPU_UTIL = parseFloat(item.CPU_UTIL).toFixed(2) + '%';
            item.MIPS = parseFloat(item.MIPS).toFixed(2);
            item.PERFORMANCE = parseFloat(item.PERFORMANCE).toFixed(2);
            item.EVALUATION = parseFloat(item.EVALUATION).toFixed(2);
            item.EVAL_ERR_RATE = (parseFloat(item.EVAL_ERR_RATE) * 100).toFixed(2) + '%';
        });
    }
  },
}
</script>

<style scoped>
</style>