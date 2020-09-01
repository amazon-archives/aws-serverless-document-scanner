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
  <div class="imageUpload">
      <image-uploader
        :preview="false"
        :className="['fileinput', { 'fileinput--loaded': hasImage }]"
        capture="environment"
        :debug="1"
        doNotResize="gif"
        :autoRotate="true"
        outputFormat="blob"
        @input="setImage"
      >
        <label for="fileInput" slot="upload-label">
          <div>
            <Icon v-bind:style="{ color: activeColor }" name="image" scale="2" />
            <p class="upload-caption">{{
              hasImage ? "Replace" : "Add image"
            }}</p>
          </div>
        </label>
      </image-uploader>
  </div>
</template>

<script>
import ImageUploader from 'vue-image-upload-resize'
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons/image'

export default {
  name: 'ImageUpload',
  components: {
    ImageUploader,
    Icon
  },
  data() {
    return {
      activeColor: '#f90',
      hasImage: false,
      image: null
    }
  },
  props: ['clear'],
  watch: { 
    clear: function(val) { 
      if(val) {
        this.activeColor = '#f90';
        this.hasImage = false;
        this.image = null;
      }
    }
  },
  methods: {
    setImage: function(output) {
      this.activeColor = '#4ac76b';
      this.hasImage = true;
      this.image = output;
      this.$emit('imageData', output)
    }
  }
}
</script>


<style>

  #fileInput {
    display: none;
  }

</style>

<style scoped>


</style>