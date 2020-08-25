<template>
    <div id="app">
      <div v-if="!signedIn">
         <amplify-authenticator></amplify-authenticator>
      </div>
      <div v-if="signedIn">
        <amplify-sign-out class="signout" v-bind:signOutOptions="signOutOptions"></amplify-sign-out>
        <DocumentScanner />
      </div>
    </div>
</template>

<script>
import DocumentScanner from './components/DocumentScanner.vue'
import { AmplifyEventBus, components } from 'aws-amplify-vue'
import { Auth } from 'aws-amplify'

import * as AmplifyVue from 'aws-amplify-vue'

const signOutOptions = {
  msg: 'You are currently signed in.',
  signOutButton: 'Sign Out'
}

export default {
  name: 'app',
  components: {
    components,
    DocumentScanner
  },
  async beforeCreate() {
    try {
      const user = await Auth.currentAuthenticatedUser()
      this.signedIn = true
    } catch (err) {
      this.signedIn = false
    }
    AmplifyEventBus.$on('authState', info => {
      console.log(info)
      if (info === 'signedIn') {
        this.signedIn = true
      } else {
        this.signedIn = false
      }
    });
  },
  data () {
    return {
      signOutOptions,
      signedIn: false
    }
  }
}
</script>

<style>
body {
  margin: 0
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  max-width: 599px;
  margin: 0 auto;
}
.signout {
  background-color: #ededed;
  margin: 0;
  padding: 11px 0px 1px;
}
</style>