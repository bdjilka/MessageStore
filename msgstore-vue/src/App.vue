<template>
  <v-app id="app" dark>
    <router-view/>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  created() {

  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff;
  position: relative;
}
</style>
