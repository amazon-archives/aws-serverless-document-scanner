// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

// Permission is hereby granted, free of charge, to any person obtaining a copy of
// this software and associated documentation files (the "Software"), to deal in
// the Software without restriction, including without limitation the rights to
// use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
// the Software, and to permit persons to whom the Software is furnished to do so.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
// FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
// COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
// IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
// CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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