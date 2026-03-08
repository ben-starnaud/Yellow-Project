<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-white text-secondary" height-hint="64">
      <q-toolbar class="q-px-lg" style="height: 64px">
        <q-btn flat no-caps no-ripple class="q-pa-none" to="/">
          <img 
            src="~assets/logo.png" 
            style="height: 40px; width: auto;"
            alt="Yellow Logo"
          >
        </q-btn>

        <q-space />

        <div class="gt-xs q-gutter-md">
          <q-btn flat no-caps label="Home" to="/" class="text-weight-bold" />
          <q-btn flat no-caps label="Purpose" class="text-weight-bold" />
          <q-btn 
            unelevated 
            color="primary" 
            text-color="secondary" 
            label="Join Us" 
            class="text-weight-bolder rounded-borders q-px-md" 
          />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
// No extra logic needed for the basic layout header
</script>

<style lang="scss">
.rounded-borders {
  border-radius: 8px;
}
</style>