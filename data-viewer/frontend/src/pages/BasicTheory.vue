<template>
  <v-card outlined tile class="pt-5 pb-3 pl-3">
    <v-row no-gutters>
      <v-col md="10" offset-md="1">
        <div align="start">
          <p><strong>CPI Model:</strong> &emsp; <var>CPI</var> = <var>CPI_cache</var> + <var>MPI</var> ∗ <var>MP</var> ∗ <var>BF</var> &emsp; <small>[1]</small></p>
          <p><strong>Performance Model:</strong> &emsp; <var>Performance</var> = <var>(CPU_freq * cores * PU)</var> / <var>(pathlength * CPI)</var> &emsp; <small>[2]</small></p>
          <p><strong>Analysis Model:</strong> &emsp; <var>Performance</var> = <var>F(CoreNum,Corefreq,UncoreFreq,LLCSize,MemSpeed, ..)</var> &emsp; <small>[3]</small></p>
        </div>
      </v-col>
    </v-row>
    <dl>
      <dt>
        <strong>CPI Cache:</strong> <span>{{ cpiCache }}</span>
        <strong>BF:</strong> <span>{{ bf }}</span>
      </dt>
    </dl>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    cpiCache: 0.00,
    bf: 0.00,
  }),
  methods: {
    updateCpiModelResult () {
      this.$http.post('/cpi/model', this.config).then(resp => {
        let cpiModelResult = resp.data;
        this.cpiCache = parseFloat(cpiModelResult.ccpi).toFixed(2);
        this.bf = parseFloat(cpiModelResult.bf).toFixed(2);
      }).catch(() => {
      });
    },
  },
  computed: {
    config: function () {
        let { workload, sku, smt, ...others} = this.$root.$data.sharedState.config;
        let config = {
            workload: workload,
            sku: sku,
            smt: smt,
            memory_speed: 'All',
            llc: 'All',
            cores: 'All',
            core_frequency: 'All',
            uncore_frequency: 'All',
        };
        return config;
    }
  },
  watch: {
    config: {
      deep: true,
      handler: function (val, oldVal) {
        this.updateCpiModelResult();
      }
    }
  }
}
</script>

<style scoped>
  dt > span {
    background: #FF0033;
    color: white;
  }
</style>
