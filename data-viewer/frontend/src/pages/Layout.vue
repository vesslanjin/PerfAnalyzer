<template>
  <v-app id="inspire">

    <!-- Navigation -->
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <template v-for="(item, i) in items">
          <v-row v-if="item.heading" :key="i" align="center">
            <v-col cols="6">
              <v-subheader v-if="item.heading">{{ item.heading }}</v-subheader>
            </v-col>
            <v-col cols="6" class="text-right">
              <v-btn small text>edit</v-btn>
            </v-col>
          </v-row>
          <v-divider v-else-if="item.divider" :key="i" dark class="my-4" />
          <v-list-item link v-else :key="i">
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ item.text }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <!-- Bar -->
    <v-app-bar
      app
      clipped-left
      color="blue-grey"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title>Performance analyzer</v-toolbar-title>
    </v-app-bar>

    <!-- Container -->
    <v-content class="pt-0">
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col>

            <!-- Content-->
            <basic-theory/>
            <mips-list/>
            <workload-information/>
            <scaling-analysis/>
            <performance-modeling/>
            <performance-evaluation/>

          </v-col>
        </v-row>
      </v-container>
    </v-content>

    <!-- Footer -->
    <v-footer
      app
      color="blue-grey"
    >
      <span>Intel</span>
      <v-spacer />
      <span>&copy; {{ year }}</span>
    </v-footer>

  </v-app>
</template>

<script>
  import menu from '@/menu'
  import BasicTheory from '@/pages/BasicTheory'
  import MipsList from '@/pages/MipsList'
  import WorkloadInformation from '@/pages/WorkloadInformation'
  import ScalingAnalysis from '@/pages/ScalingAnalysis'
  import PerformanceModeling from '@/pages/PerformanceModeling'
  import PerformanceEvaluation from '@/pages/PerformanceEvaluation'

  export default {
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
      year: '2020',
    }),
    created () {
      this.year = this.currentYear();
    },
    computed: {
      items () {
        return menu;
      },
    },
    methods: {
      currentYear () {
        let date = new Date();
        return date.getFullYear();
      }
    },
    components: {
      BasicTheory,
      MipsList,
      WorkloadInformation,
      ScalingAnalysis,
      PerformanceModeling,
      PerformanceEvaluation,
    },
  }
</script>

<style scoped>
</style>
