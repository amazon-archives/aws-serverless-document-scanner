<template>
  <div class="pageSelector">
    <Icon class="iconButton" name="chevron-left" scale="2" v-on:click="previous()" />
    <input class="pageNumber" v-model="pageNumber" type="number" />
    <Icon class="iconButton" name="chevron-right" scale="2" v-on:click="next()" />
  </div>
</template>

<script>

import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons/chevron-right'
import 'vue-awesome/icons/chevron-left'

export default {
  name: 'ProjectList',
  components: {
    Icon
  },
  data() {
    return {
      pageNumber: 1
    }
  },
  props: ['page'],
  watch: { 
    page: function(val) { 
      this.pageNumber = val;
    }
  },
  methods: {
    previous: function () {
      if(this.pageNumber <= 1) { return }
      this.pageNumber = this.pageNumber - 1
      this.$emit('update', this.pageNumber)
    },
    next: function () {
      this.pageNumber = this.pageNumber + 1
      this.$emit('update', this.pageNumber)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .pageNumber {
    max-width: 60px;
    border: none;
    background: transparent;
    border-bottom: 1px solid #fff;
    outline: none;
    font-family: Tahoma, Geneva, sans-serif;
    color: #FF9900;
    font-size: 24px;
    text-align: center;
  }

  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  input[type=number] {
    -moz-appearance: textfield;
  }

  .iconButton {
    color: #f90;
  }
</style>