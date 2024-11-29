<template>
  <HomeLayout>
    <div class="container my-3" style="min-height: 80vh">
      <div class="row justify-content-center">
        <div class="col-xl-6 col-lg-8 col-md-10 shadow p-3">
          <h3 class="text-primary">Publish New Event</h3>
          <!-- progressbar -->
          <div class="progress my-3" role="progressbar">
            <div
              class="progress-bar progress-bar-striped bg-primary"
              :style="{ width: ((step - 1) / 3) * 100 + '%' }"></div>
          </div>
          <!-- fieldsets -->
          <fieldset v-show="step === 1">
            <div class="mb-3">
              <label for="validationCustom01" class="form-label">Title</label>
              <input
                type="text"
                class="form-control"
                v-model="formData.title"
                placeholder="Workshop..."
                value=""
                required />
            </div>
            <div class="mb-3">
              <label for="validationCustom01" class="form-label">Poster</label>
              <input
                type="file"
                class="form-control"
                @change="inputPoster"
                accept="image/*"
                required />
            </div>
            <div class="mb-3">
              <label for="validationCustom01" class="form-label">Event Date</label>
              <input
                type="date"
                class="form-control"
                v-model="formData.start_date"
                value=""
                required />
            </div>
            <!-- <div class="mb-3">
              <label for="validationCustom01" class="form-label">
                End Date
                <span class="small text-secondary">
                  (leave it blank if the event is one-day event)
                </span>
              </label>
              <input type="date" class="form-control" v-model="formData.end_date" value="" />
            </div> -->
            <div class="d-block mt-3">
              <button class="btn btn-warning" v-on:click="nextStep">next</button>
            </div>
          </fieldset>
          <fieldset v-show="step === 2">
            <label for="eventDescription" class="form-label"
              >Tell us everything about this event</label
            >
            <div class="editor-container card bg-light">
              <!-- Menu bar -->
              <div
                class="editor-menu-bar btn-toolbar d-flex justify-content-between"
                role="toolbar">
                <!-- Font -->
                <div class="btn-group me-2" role="group">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleBold().run()"
                    :class="{ 'active btn-primary text-white': editor?.isActive('bold') }">
                    <i class="fas fa-bold"></i>
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleItalic().run()"
                    :class="{ 'active btn-primary text-white': editor?.isActive('italic') }">
                    <i class="fas fa-italic"></i>
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleStrike().run()"
                    :class="{ 'active btn-primary text-white': editor?.isActive('strike') }">
                    <i class="fas fa-strikethrough"></i>
                  </button>
                </div>
                <!-- Heading -->
                <div class="btn-group me-2" role="group">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
                    :class="{
                      'active btn-primary text-white': editor?.isActive('heading', { level: 1 }),
                    }">
                    <i class="fas fa-heading"></i> H1
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
                    :class="{
                      'active btn-primary text-white': editor?.isActive('heading', { level: 2 }),
                    }">
                    <i class="fas fa-heading"></i> H2
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
                    :class="{
                      'active btn-primary text-white': editor?.isActive('heading', { level: 3 }),
                    }">
                    <i class="fas fa-heading"></i> H3
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleHeading({ level: 4 }).run()"
                    :class="{
                      'active btn-primary text-white': editor?.isActive('heading', { level: 4 }),
                    }">
                    <i class="fas fa-heading"></i> H4
                  </button>
                </div>
                <!-- Lists -->
                <div class="btn-group" role="group">
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleBulletList().run()"
                    :class="{ 'active btn-primary text-white': editor?.isActive('bulletList') }">
                    <i class="fas fa-list-ul"></i>
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editor.chain().focus().toggleOrderedList().run()"
                    :class="{ 'active btn-primary text-white': editor?.isActive('orderedList') }">
                    <i class="fas fa-list-ol"></i>
                  </button>
                </div>
              </div>
              <!-- Editor content -->
              <div class="editor-content bg-white p-3" style="min-height: 200px">
                <editor-content :editor="editor" class="editor" v-if="editor" />
              </div>
            </div>

            <div class="d-block mt-3">
              <button class="btn btn-outline-secondary me-2" v-on:click="prevStep">prev</button>
              <button class="btn btn-warning" v-on:click="nextStep">next</button>
            </div>
          </fieldset>
          <fieldset v-show="step === 3">
            <label for="eventImage" class="form-label">
              Give us picture about this event, such as road map etc.
              <span class="small text-secondary">
                (optional)
              </span>
            </label>
            <file-pond
              name="test"
              ref="pond"
              class-name="my-pond"
              label-idle="Drop files here..."
              allow-multiple="true"
              accepted-file-types="image/jpeg, image/png"
              v-bind:files="myFiles"
              v-on:init="handleFilePondInit" />
            <div class="d-block mt-3">
              <button class="btn btn-outline-secondary me-2" v-on:click="prevStep">prev</button>
              <button class="btn btn-primary" v-on:click="submitForm">Submit</button>
            </div>
          </fieldset>
          <fieldset v-show="step === 4">
            <div class="row my-5 justify-content-center">
              <button v-on:click="linkPendaftaran" class="col-6 btn btn-primary">Add a registration link</button>
            </div>
            <div class="row text-center">
              <router-link :to="'/home'">Lihat event</router-link>
            </div>
          </fieldset>
        </div>
      </div>
    </div>
  </HomeLayout>
</template>

<script>
import HomeLayout from "@/views/HomeLayout.vue";
// Tiptap
import { Editor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import Heading from "@tiptap/extension-heading";
import BulletList from "@tiptap/extension-bullet-list";
import OrderedList from "@tiptap/extension-ordered-list";
// Filepond
import vueFilePond from "vue-filepond";
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js";
import FilePondPluginImagePreview from "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.esm.js";
import "filepond/dist/filepond.min.css";
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css";
import { setOptions } from "filepond";
import Swal from "sweetalert2";
import axios from "axios";

const FilePond = vueFilePond(FilePondPluginFileValidateType, FilePondPluginImagePreview);

export default {
  name: "CreateEvent",
  components: {
    HomeLayout,
    EditorContent,
    FilePond,
  },
  data() {
    return {
      step: 1,
      formData: {
        title: "",
        start_date: "",
        end_date: "",
      },
      eventId: "",
      editor: null,
      posterFile: null,
      myFiles: null,
    };
  },
  methods: {
    inputPoster(event) {
      const file = event.target.files[0];
      if (file) {
        this.posterFile = file;
        console.log("File masok.");
      } else {
        console.error("Tidak ada file yang dipilih.");
      }
    },
    handleFilePondInit: function () {
      console.log("FilePond has initialized");

      this.$refs.pond.getFiles();
    },
    nextStep() {
      this.step++;
    },
    prevStep() {
      this.step--;
    },
    async submitForm() {
      if (!this.formData.title || !this.posterFile || !this.formData.start_date || !this.editor?.getHTML()?.trim()) {
        Swal.fire({
          title: "Error!",
          text: "Lengkapi seluruh data!",
          icon: "error",
          customClass: {
            popup: "alert alert-danger",
            title: "h4",
            content: "small",
            confirmButton: "btn btn-danger",
          },
          buttonsStyling: false,
        });
        return;
      }

      const formData = new FormData();
      formData.append("title", this.formData.title);
      formData.append("poster", this.posterFile);
      formData.append("start_date", this.formData.start_date);
      formData.append("end_date", this.formData.end_date);
      formData.append("description", this.editor ? this.editor.getHTML() : "");
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${process.env.VUE_APP_BACKEND}/event`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        const result = await response.json();

        this.eventId = result.id;
        console.log("id:",this.eventId);
        this.step++;
      } catch (error) {
        console.error(error);
        alert("Error submitting form.");
      }
    },

    async linkPendaftaran() {
      Swal.fire({
        title: "Paste your registration form here",
        input: "text",
        inputPlaceholder: "https://forms.gle/XXXXX",
        inputAttributes: {
          autocapitalize: "off",
          class: "form-control"
        },
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-save"></i> Save',
        cancelButtonText: '<i class="fas fa-cancel"></i> Cancel',
        footer: '<a id="open-google-forms" class="text-primary" href="https://forms.google.com" target="_blank"><i class="fas fa-external-link-alt"></i> Create Google Form</a>',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-primary",
          cancelButton: "btn btn-secondary"
        },
        showLoaderOnConfirm: true,
        preConfirm: async (link) => {
          if (!link) {
            Swal.showValidationMessage("Url can't be empty");
            return;
          }

          try {
            const token = localStorage.getItem("token");
            const response = await axios.patch(`${process.env.VUE_APP_BACKEND}/update/event`,
              {
                id: this.eventId,
                key: 'registration_url',
                value: link
              },
              {
                  headers: {
                      Authorization: `Bearer ${token}`,
                      'Content-Type': 'application/json',
                  }
              }
            );

            if (response.status !== 200) {
              Swal.showValidationMessage(`Gagal menyimpan: ${response.data.message || "Error"}`);
            }
            return response.data;
          } catch (error) {
            Swal.showValidationMessage(`Request failed: ${error.response?.data?.message || error.message}`);
          }
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: "Success!",
            text: `${result.value.message}`,
            icon: "success",
          });
        }
      });
    }
  },
  mounted() {
    this.editor = new Editor({
      content: "<p>This is...</p>",
      extensions: [
        StarterKit,
        Heading.configure({
          levels: [1, 2, 3, 4],
        }),
        BulletList,
        OrderedList,
      ],
    });
    this.editor.on("focus", () => {
      this.$el.querySelector(".ProseMirror").style.outline = "none";
    });

    setOptions({
      server: {
        process: {
          url: `${process.env.VUE_APP_BACKEND}/file/upload`,
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          onload: (response) => {
            const { image_id } = JSON.parse(response);
            return image_id;
          },
        },
        revert: {
          url: `${process.env.VUE_APP_BACKEND}/file/delete`,
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        },
      },
      allowMultiple: true,
    });
  },
  beforeUnmount() {
    this.editor.destroy();
  },
};
</script>
