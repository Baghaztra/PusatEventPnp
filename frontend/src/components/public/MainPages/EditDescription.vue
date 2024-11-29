<template>
  <HomeLayout>
    <div class="container my-3" style="min-height: 80vh">
      <div class="row justify-content-center">
        <div class="col-xl-6 col-lg-8 col-md-10 shadow p-3">
          <h3 class="text-primary">Edit Event Description</h3>
          <div class="editor-container card bg-light">
            <!-- Menu bar -->
            <div class="editor-menu-bar btn-toolbar d-flex justify-content-between" role="toolbar">
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
            <button class="btn btn-outline-secondary me-2" @click="this.$router.go(-1)">
              Cancel
            </button>
            <button class="btn btn-primary" v-on:click="submitForm">Submit</button>
          </div>
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
import Swal from "sweetalert2";
import axios from "axios";
import router from "@/router";

export default {
  name: "EventDetails",
  components: {
    HomeLayout,
    EditorContent,
  },
  props: {
    id: String,
  },
  data() {
    return {
      editor: null,
    };
  },
  methods: {
    async initEditor() {
      this.loading = true;
      try {
        const description = await this.getDesc(); // Tunggu hasil getDesc
        this.editor = new Editor({
          content: description || '', // Pastikan ada default jika deskripsi kosong
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
      } catch (error) {
        console.error("Error initializing editor:", error);
      } finally {
        this.loading = false;
      }
    },

    async getDesc() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/event/${this.id}`);
        return response.data.description || ""; // Kembalikan string kosong jika tidak ada deskripsi
      } catch (error) {
        console.error("Error fetching event details:", error);
        return ""; // Default jika gagal mengambil deskripsi
      }
    },

    async submitForm() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.patch(
          `${process.env.VUE_APP_BACKEND}/update/event`,
          {
            id: this.id,
            key: 'description',
            value: this.editor ? this.editor.getHTML() : "",
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        if (response.status !== 200) {
          Swal.showValidationMessage(`Gagal menyimpan: ${response.data.message || "Error"}`);
        }
        router.push(`/event/${this.id}`)
        return response.data;
      } catch (error) {
        Swal.showValidationMessage(
          `Request failed: ${error.response?.data?.message || error.message}`
        );
      }
    },
  },
  mounted() {
    this.initEditor();
  },
  beforeUnmount() {
    this.editor.destroy();
  },
};
</script>
