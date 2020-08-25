<template>
  <div class="ProjectList">
    Projects 
    <Icon 
      name="caret-down"
      v-on:click="hide()"
      v-if="showList" 
      scale="1" 
    />
    <Icon 
      name="caret-right"
      v-on:click="show()"
      v-if="!showList" 
      scale="1" 
    /> 
    <div v-if="showList">
      <span v-for="project in projects" v-bind:key="project.project_name">  
        <p class="pItem" v-on:click="select(project)">
          {{project.project_name}}
        </p>    
      </span>
    </div>
  </div>
</template>

<script>

import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons/caret-right'
import 'vue-awesome/icons/caret-down'


export default {
  name: 'ProjectList',
  components: {
    Icon
  },
  data() {
    return {
      projects: [],
      showList: true
    }
  },
  props: ['projectList'],
  watch: { 
    projectList: function(val) { 
      console.log(val)
      this.projects = val;
    }
  },
  methods: {
    select: function (project) {
      this.$emit('select', project)
    },
    hide: function () {
      this.showList = false
    },
    show: function () {
      this.showList = true
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.pItem {
  background-color: #f90;
  color: white;
  max-width: 300px;
  margin: 0 auto;
  border-style: solid;
  border-color: white;
  border-width: 2px;
}

.deleteButton {
  margin-left: 20%;
}

</style>