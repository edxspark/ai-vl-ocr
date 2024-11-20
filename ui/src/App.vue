<template>
  <div id="app">
    <AIVLOCR msg="Welcome to AI-VL-OCR" />
  </div>
</template>

<script>
import AIVLOCR from './components/AIVLOCR.vue'

export default {
  name: 'App',
  components: {
    AIVLOCR
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

</style>
