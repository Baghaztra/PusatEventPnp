<template>
  <AdminLayout>
    <div class="container-fl">
      <p v-if="accounts && accounts.length === 0">Data tidak tersedia atau sedang dimuat...</p>
      <div v-else class="card p-3">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="(item, index) in items" :key="index">
              <td>{{ item.username }}</td>
              <td>
                <span :class="{
                  'badge': true,
                  'text-bg-success': item.status == 'Active',
                  'text-bg-danger': item.status != 'Active'
                }">
                  {{ item.status }}
                </span>
              </td>
              <td>
                <a href="#" class="btn btn-sm btn-danger d-inline me-2"><i class="fas fa-ban"></i> Ban</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </AdminLayout>
</template>

<script>
import axios from "axios";
import AdminLayout from "@/views/AdminLayout.vue";

export default {
  name: "AdminEvents",
  components: {
    AdminLayout,
  },
  data() {
    return {
      items: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/users`);
        this.items = Array.isArray(response.data) ? response.data : [];
        // console.log("Data fetched:", this.items);
      } catch (error) {
        console.error("Error fetching data:", error);
        this.items = [];
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
</style>
