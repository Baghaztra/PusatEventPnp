<template>
  <HomeLayout>
    <div class="container my-3">
      <div class="row justify-content-center">
        <div class="col-xl-6 col-lg-8 col-md-10 shadow p-3">
          <h3 class="text-primary">Publish New Event</h3>
          <!-- progressbar -->
          <div class="progress my-3" role="progressbar">
            <div class="progress-bar progress-bar-striped bg-primary" :style="{ width: ((step-1) / 3) * 100 + '%' }"></div>
          </div>
          <!-- fieldsets -->
          <fieldset v-show="step === 1">
            <label for="validationCustom01" class="form-label">Title</label>
            <input type="text" class="form-control" value="" required>
            <div class="invalid-feedback">
              Input event's title
            </div>
            <div class="d-block mt-3">
              <button class="btn btn-warning" v-on:click="nextStep">next</button>
            </div>
          </fieldset>
          <fieldset v-show="step === 2">
            <label for="eventDescription" class="form-label">Description</label>
            <ckeditor
              :editor="editor"
              v-model="formData.description"
              :config="editorConfig"
            ></ckeditor>
            <div class="d-block mt-3">
              <button class="btn btn-outline-secondary me-2" v-on:click="prevStep">prev</button>
              <button class="btn btn-warning" v-on:click="nextStep">next</button>
            </div>
          </fieldset>
          <fieldset v-show="step === 3">
            <label for="eventImage" class="form-label">Event Image</label>
            <input type="file" id="eventImage" class="form-control" @change="handleFileUpload">
            <div class="d-block mt-3">
              <button class="btn btn-outline-secondary me-2" v-on:click="prevStep">prev</button>
              <button class="btn btn-primary" v-on:click="submitForm">Submit</button>
            </div>
            <div class="d-block mt-3">
              <button class="btn btn-outline-secondary me-2" v-on:click="prevStep">prev</button>
              <button class="btn btn-primary" v-on:click="submitForm">Submit</button>
            </div>
          </fieldset>
          <fieldset v-show="step === 4">Form Success</fieldset>
        </div>
      </div>
    </div>
  </HomeLayout>
</template>

<script>
import HomeLayout from "@/views/HomeLayout.vue";
import { CKEditor } from "@ckeditor/ckeditor5-vue";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

export default {
  name: "CreateEvent",
  components: {
    HomeLayout,
    CKEditor
  },
  data() {
    return {
      step: 1,
      formData: {
        title: "",
      },
      editor: ClassicEditor, // Instance CKEditor
      editorConfig: {
        toolbar: ["heading", "|", "bold", "italic", "link", "bulletedList", "numberedList", "|", "undo", "redo"],
      },
      selectedFile: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    nextStep() {
      this.step++;
    },
    prevStep() {
      this.step--;
    },
    async submitForm() {
      if (!this.selectedFile) {
        alert("Please upload an image!");
        return;
      }

      const event = new FormData();
      event.append("title", this.formData.title);
      event.append("image", this.selectedFile);

      try {
        const response = await fetch("https://your-backend-url/api/events", {
          method: "POST",
          body: event,
        });

        if (!response.ok) {
          throw new Error("Failed to submit form");
        }

        const result = await response.json();
        alert("Form submitted successfully!");
        console.log(result);
        this.step++;
      } catch (error) {
        console.error(error);
        alert("Error submitting form.");
      }
    },
  },
};
</script>
