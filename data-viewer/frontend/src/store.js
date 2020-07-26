var store = {
    debug: false,
    state: {
      config: {},
      cpiDetailsListChanged: false,
      performanceModelingGlm: {},
    },
    setConfigAction (newValue) {
      if (this.debug) console.log('setConfigAction triggered with', newValue)
      this.state.config = newValue
    },
    setcpiDetailsListChangedAction (newValue) {
      if (this.debug) console.log('setcpiDetailsListChangedAction triggered with', newValue)
      this.state.cpiDetailsListChanged = newValue
    },
    setperformanceModelingGlm (newValue) {
      if (this.debug) console.log('setperformanceModelingGlm triggered with', newValue)
      this.state.performanceModelingGlm = newValue
    },
}
export default store;