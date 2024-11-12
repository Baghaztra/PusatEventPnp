<template>
    <AdminLayout>
      <div class="container-fl">
        <!-- Tampilkan pesan jika data tidak tersedia -->
        <p v-if="accounts && accounts.length === 0">Data tidak tersedia atau sedang dimuat...</p>
  
        <!-- Tampilkan tabel jika ada data -->
        <table v-else class="table table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="item in accounts" :key="item.id"> <!-- Gunakan item.id sebagai key -->
              <td>{{ item.username }}</td>
              <td>{{ item.email }}</td>
              <td>{{ item.status }}</td>
              <td>
                <a href="#" class="btn btn-sm btn-danger" @click="deleteData(item.id)">Delete</a>
                <a href="#" class="btn btn-sm btn-danger" @click="updateData(item.id)">Update</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </AdminLayout>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import AdminLayout from "@/views/AdminLayout.vue";
  
  export default {
    name: "AdminEventorganizers",
    components: {
      AdminLayout,
    },
    setup() {
      const accounts = ref([]); // Inisialisasi sebagai array kosong
  
      const fetchData = async () => {
        try {
          const response = await axios.get(`http://localhost:5000/event_organizers`);
          const data = response.data; 
  
          console.log("Data fetched:", data); 
          accounts.value = Array.isArray(data) ? data : [];
        } catch (error) {
          console.error("Error fetching data:", error);
          accounts.value = [];
        }
      };
      // const editData = async (id) => {
      //   try {
      //     const response = await axios.get(`http://localhost:5000/users?id=${id}`);
      //     const data = response.data; 
  
      //     console.log("Data fetched:", data); 
      //   } catch (error) {
      //     console.error("Error fetching data:", error);
      //   }
      // };
      // const updateData = async (id) => {
      //   try {
      //     const response = await axios.put(`http://localhost:5000/users`);
      //     const data = response.data; 
  
      //     console.log("Data fetched:", data); 
      //   } catch (error) {
      //     console.error("Error updating data:", error);
      //   }
      // };
      // const deleteData = async (id) => {
      //   try {
      //     const response = await axios.delete(`http://localhost:5000/users?id=${id}`);
      //     const data = response.data; 
  
      //     console.log("Data fetched:", data); 
      //   } catch (error) {
      //     console.error("Error updating data:", error);
      //   }
      // };
  
      onMounted(() => {
        fetchData();
      });
  
      return {
        accounts,
      };
    },
  };
  </script>
  
  <style>
  </style>
  