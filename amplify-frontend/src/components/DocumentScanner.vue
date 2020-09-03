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
  <div class="documentScanner">
    <div class="ds">
      <div class="logo">
        <Icon name="file-alt" color="#f90" scale="3" />
        <div class="logoText"><h3>Document<br />Scanner</h3></div>
      </div>
      
      <input v-model="projectName" />
      <button v-on:click="create(projectName)">
        Create Project
      </button>

      <div class="projectData" v-show="projects">
        <ProjectList 
          @select="selectProject"
          v-bind:project-list="projects"
          v-show="projects != null"
          ref="projectListRef"
        />
        <Project 
          v-bind:project="selectedProject"
          v-bind:count="pageCount"
          v-bind:username="username"
          @delete="deleteProject"
          @generate="generatePDF"
        />

        <button v-show="pdfURI" v-on:click="openPDF()">
          Open in new window
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons/file-alt'
import { Auth, API } from 'aws-amplify'
import ProjectList from './ProjectList.vue'
import download from 'downloadjs'
import Project from './Project.vue'


let apiName = 'DocumentScannerAPI';

export default {
  name: 'DocumentScanner',
  components: {
    ProjectList,
    Project,
    Icon
  },
  data() {
    return {
      projects: null,
      selectedProject: null,
      pageCount: null,
      projectName: null,
      photos: null,
      username: null,
      identityId: null,
      pdfURI: null
    }
  },
  async mounted() {
    this.getProjects()
    let currentCredentials = await Auth.currentCredentials()
    let currentUser = await Auth.currentAuthenticatedUser()

    this.username = currentUser.username
    this.identityId = currentCredentials.data.IdentityId
  },
  methods: {
    create: async function (name) {
      let path = '/projects';
      let myInit = {
        body: {
          name: name
        }
      }
      await API.post(apiName, path, myInit);
      this.getProjects()
      return this.$refs.projectListRef.show()  
    },
    deleteProject: async function (name) {
      let path = '/projects/delete';
      let myInit = {
        body: {
          name: name,
          identityId: this.identityId
        }
      }

      console.log(myInit)
      await API.post(apiName, path, myInit);
      this.selectedProject = null
      return this.getProjects()
    },
    getProjects: function () {
      let path = '/projects';

      API
        .get(apiName, path, {})
        .then(response => {
          console.log(response)
          if(response.length > 0){
            this.projects = response;
          }else {
            this.projects = null;
          }
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    getPageCount: function (name) {
      let path = `/pages/count/${name}`;
      
      API
        .get(apiName, path, {})
        .then(response => {
          console.log(response)
          this.pageCount = response.page_count
        })
        .catch(error => {
          console.log(error.response);
        });
    },
    openPDF: function () {
      let pdfWindow = window.open("")
      pdfWindow.document.write(
          "<iframe width='100%' height='100%' src='" + this.pdfURI + "'></iframe>"
      )
    },
    generatePDF: function (name) {
      let path = `/pages/pdf/${name}`;
      setTimeout(() => {  
        API
        .get(apiName, path, {})
        .then(response => {
          this.pdfURI = response.url
          download(this.pdfURI, this.selectedProject.project_name + ".pdf", "application/pdf");
        })
        .catch(error => {
          console.log(error.response);
        });
      }, 2000);
    },
    selectProject: function (project) {
      this.pdfURI = null
      this.getPageCount(project.project_name)
      this.selectedProject = project
      this.$refs.projectListRef.hide()  
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logoText {
  display: flex;
  text-align: left;
  margin-left: 10px;
}

.documentScanner {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  padding-bottom: 10%;
}

button {
  min-width: 45px;
  display: inline-block;
  margin-bottom: 0;
  margin: 5px;
  vertical-align: middle;
  touch-action: manipulation;
  cursor: pointer;
  user-select: none;
  color: #fff;
  background-color: #f90;
  border-color: #ccc;
  padding: 5px 5px;
  border: none;
  border-radius: 2px;
}
button:active {
  opacity: 1;
  background-color: var(--button-click);
}
button:hover {
  opacity: 0.8;
}

</style>