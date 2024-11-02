<template>
  <AdminLayout>
    <div class="container-fl">
      <!-- Tampilkan pesan jika data tidak tersedia -->
      <p v-if="itemsSearching.length === 0">Data tidak tersedia atau sedang dimuat...</p>

      <!-- Tampilkan tabel jika ada data -->
      <table v-else class="table table-striped">
        <thead>
          <tr>
            <th>Title</th>
            <th>Event Organizer</th>
            <th>Event Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(item, index) in itemsSearching" :key="index">
            <td>{{ item.title }}</td>
            <td>{{ item.eo }}</td>
            <td>{{ item.event_date }}</td>
            <td>{{ item.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminLayout>
</template>

<script>
import { ref, onMounted } from "vue";
import AdminLayout from "@/views/AdminLayout.vue";

export default {
  name: "AdminEvents",
  components: {
    AdminLayout,
  },
  setup() {
    const itemsSearching = ref([]); // Inisialisasi sebagai array kosong

    // Fungsi fetch data
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/event-latest?per_page=10000`);
        const data = await response.json();
        
        itemsSearching.value = Array.isArray(data.events) ? data.events : [];
        console.log("Data fetched:", itemsSearching.value); // Lakukan logging di sini
      } catch (error) {
        console.error("Error fetching data:", error);
        itemsSearching.value = []; // Set ke array kosong jika error terjadi
      }
    };

    onMounted(() => {
      fetchData(); // Ambil data saat komponen dipasang
    });

    return {
      itemsSearching,
    };
  },
};
</script>

<style>
/* table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
  text-align: left;
} */
</style>
