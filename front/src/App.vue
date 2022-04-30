<template>
  
  <div class="col-lg-8 mx-auto p-3 py-md-5">
  <header class="d-flex align-items-center pb-3 mb-5 border-bottom">
      <span class="fs-4">GOV Procurement Portal</span>

      <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
        <router-link class="me-3 py-2 text-dark text-decoration-none" to="/">Procurement</router-link>
        <router-link class="me-3 py-2 text-dark text-decoration-none" to="/supplier">Suppliers</router-link>
        <router-link class="me-3 py-2 text-dark text-decoration-none" to="/agency">Agency</router-link>
      </nav>
  </header>

  <main>
    <router-view></router-view>
  </main>
</div>

</template>

<script>

export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
