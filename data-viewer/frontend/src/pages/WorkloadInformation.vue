<template>
  <v-card outlined tile class="mt-3">
    <v-form v-model="valid">
      <v-container>
        <v-row>
          <v-col cols="6" sm="2" offset-sm="2">
            <v-select label="Workload" :items="configSettings.workload" v-model="config.workload"></v-select>
          </v-col>
          <v-col cols="6" sm="2">
            <v-select label="SKU" :items="configSettings.sku" v-model="config.sku"></v-select>
          </v-col>
          <v-col cols="6" sm="2">
            <v-select label="SMT" :items="configSettings.smt" v-model="config.smt"></v-select>
          </v-col>
          <v-col cols="6" sm="2">
            <v-select label="Memory Speed" :items="configSettings.memorySpeed" v-model="config.memory_speed"></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" sm="2" offset-sm="2">
            <v-select label="LLC" :items="configSettings.llc" v-model="config.llc"></v-select>
          </v-col>
          <v-col cols="6" sm="2">
            <v-select label="Cores" :items="configSettings.cores" v-model="config.cores"></v-select>
          </v-col>
          <v-col cols="6" sm="2">
            <v-select label="Core (GHz)" :items="configSettings.coreFreq" v-model="config.core_frequency"></v-select>
          </v-col>
          <v-col cols="6" sm="2">
            <v-select label="UnCore (GHz)" :items="configSettings.uncoreFreq" v-model="config.uncore_frequency"></v-select>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
import { configSettingsData } from '@/mockDB'

export default {
  props: {
    config: {
      type: Object,
      default: () => ({
        workload: configSettingsData.workload[0],
        sku: configSettingsData.sku[0],
        smt: configSettingsData.smt[0],
        memory_speed: configSettingsData.memorySpeed[0],
        llc: configSettingsData.llc[0],
        cores: configSettingsData.cores[0],
        core_frequency: configSettingsData.coreFreq[0],
        uncore_frequency: configSettingsData.uncoreFreq[0],
      })
    },
  },
  data: () => ({
    valid: false,
    configSettings: configSettingsData,
  }),
  watch: {
    config: {
      deep: true,
      handler: function (val, oldVal) {
        this.$root.$data.sharedState.config = val;
      }
    },
  },
  created() {
    this.getSettings();
  },
  methods: {
    getSettings () {
      this.$http.get('/settings').then(resp => {
        let settings = resp.data;
        //console.log(settings);
        this.configSettings.workload = settings.workload;
        this.configSettings.sku = settings.sku;
        this.configSettings.smt = settings.smt;
        this.configSettings.memorySpeed = settings.memory_speed;
        this.configSettings.llc = settings.llc;
        this.configSettings.cores = settings.cores;
        this.configSettings.coreFreq = settings.core_frequency;
        this.configSettings.uncoreFreq = settings.uncore_frequency;
        if (settings.workload.length > 1) {
          this.config.workload = settings.workload[1];
        }
        if (settings.sku.length > 1) {
          this.config.sku = settings.sku[1];
        }
        if (settings.smt.length > 1) {
          this.config.smt = settings.smt[1];
        }
      }).catch(() => {
      });
    },
  }
}
</script>

<style scoped>
</style>
