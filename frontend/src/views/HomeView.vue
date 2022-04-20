<template>
  <div class="home">
      <HelloWorld msg="Welcome to Your Vue.js App"/>
      <img src="../assets/logo.png">
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>

<style scoped>
  img {
    width: 300px;
    height: 300px;
  }
</style>