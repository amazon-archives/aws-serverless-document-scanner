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