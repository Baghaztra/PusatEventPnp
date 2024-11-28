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
              <label for="validationCustom01" class="form-label">Start Date</label>
              <input
                type="date"
                class="form-control"
                v-model="formData.start_date"
                value=""
                required />
            </div>
            <div class="mb-3">
              <label for="validationCustom01" class="form-label"
                >End Date
                <span class="small text-secondary"
                  >(leave it blank if the event is one-day event)</span
                ></label
              >
              <input type="date" class="form-control" v-model="formData.end_date" value="" />
            </div>
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
            <label for="eventImage" class="form-label"
              >Give us picture about this event, such as road map etc.</label
            >
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
            <button v-on:click="linkPendaftaran">Tambahkan link pendaftaran</button>
            <router-link :to="'/home'">Lihat event</router-link>
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
import vueFilePond from "vue-filepond";
// Filepond
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.esm.js";
import FilePondPluginImagePreview from "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.esm.js";
import "filepond/dist/filepond.min.css";
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css";
import { setOptions } from "filepond";
import Swal from "sweetalert2";

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

        console.log(result);
        this.step++;
      } catch (error) {
        console.error(error);
        alert("Error submitting form.");
      }
    },

    async linkPendaftaran() {
      Swal.fire({
        title: "Submit your Github username",
        input: "text",
        inputAttributes: {
          autocapitalize: "off"
        },
        showCancelButton: true,
        confirmButtonText: "Look up",
        showLoaderOnConfirm: true,
        preConfirm: async (login) => {
          try {
            const githubUrl = `
              https://api.github.com/users/${login}
            `;
            const response = await fetch(githubUrl);
            if (!response.ok) {
              return Swal.showValidationMessage(`
                ${JSON.stringify(await response.json())}
              `);
            }
            return response.json();
          } catch (error) {
            Swal.showValidationMessage(`
              Request failed: ${error}
            `);
          }
        },
        allowOutsideClick: () => !Swal.isLoading()
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
            title: `${result.value.login}'s avatar`,
            imageUrl: result.value.avatar_url
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
