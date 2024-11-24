<template>
  <div>
    <div class="card p-2">
      <img
        :src="data.images[0]"
        alt="Event Image"
        class="rounded"
        style="width: 100%; aspect-ratio: 3 / 4" />
      <div class="col-body d-flex flex-column">
        <h5 class="text-primary" style="font-weight: bold">{{ data.title }}</h5>
        <span class="text-secondary">By {{ data.eo }}</span>
        <span class="text-primary">{{ formatDate(data.event_date) }}</span>
        <div class="mb-1">
          <router-link class="btn btn-primary me-1" to="">Register!</router-link>
          <router-link class="btn btn-primary" :to="`/event/${data.id}`">More</router-link>
          <button 
            class="btn"
            :class="{ 'text-primary': isLiked }"
            @click="toggleLike"
          >
            <span class="me-1">{{ data.likes?.length ?? 0 }}</span>
            <i :class="isLiked? 'fas fa-thumbs-up' : 'far fa-thumbs-up'"></i>
          </button>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "CardComponent",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isLiked: false,
      userId: null,
    };
  },
  methods: {
    async toggleLike() {
      try {
        // const response = await axios.post(
        await axios.post(
          `http://localhost:5000/like/${this.data.id}`,
          {}, // Body kosong
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        // console.log(response.data.msg);
        this.isLiked = !this.isLiked; 
        // console.log(this.isLiked);
        this.$emit('refresh-events');
        // this.isLiked = response.data.liked; 

      } catch (error) {
        console.error("Error saat mengirim permintaan like:", error);
        alert("Gagal mengubah status like.");
      }
    },
    formatDate(dateString) {
      if (!dateString) return "Tanggal tidak tersedia"; // Validasi
      const options = { weekday: "long", day: "2-digit", month: "long", year: "numeric" };
      try {
        return new Intl.DateTimeFormat("id-ID", options).format(new Date(dateString));
      } catch {
        return "Format tanggal tidak valid";
      }
    },
    truncateText(text, maxLength) {
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + "...";
      }
      return text;
    },
  },
  async created() {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        console.error("Token tidak ditemukan. User belum login.");
        return;
      }

      const response = await axios.get("http://localhost:5000/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      this.userId = response.data.user_id; // Simpan ID user
      
      this.isLiked = this.data.likes.includes(this.userId); 
    } catch (error) {
      console.error("Error saat mendapatkan profil:", error.message);
    }
  },
  mounted() {
    this.isLiked = !!this.data.isLiked;
  }
};
</script>

<style></style>
