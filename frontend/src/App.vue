<template>
  <div id="app">
    <router-view/>
    <nav>
      <router-link v-if="this.$router.currentRoute.path !='/'" to="/">Home</router-link>
      <router-link v-if="this.$router.currentRoute.path !='/setup' && this.$store.state.isLogin == true" to="/setup">| setup</router-link>
      <span> | </span>
      <router-link to="/Login" v-if="this.$store.state.isLogin == false">
        Login
      </router-link>
      <span v-if="this.$store.state.isLogin == false"> | </span>
      <a @click="logout" v-if="this.$store.state.isLogin == true">Logout</a>
      <span v-if="this.$store.state.isLogin == true"> | </span>
      <router-link v-if="this.$store.state.isLogin == false" to="/sign_up">SignUp</router-link>
    </nav>
  </div>
</template>

<script>
export default {
   name: 'app',
   components: {
  },
  methods: {
    logout() {
      document.cookie = 'token =; Max-Age=0'
      this.$store.state.isLogin = false
      this.$router.push('/')
    }
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

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
