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
                <button 
                  v-on:click="ban(item)" 
                  :class="{
                    'btn btn-sm d-inline me-2': true,
                    'btn-danger' : item.status != 'Banned',
                    'btn-success' : item.status == 'Banned'
                }">
                  <i class="fas fa-ban"></i> {{ item.status == 'Banned'? 'Activate':'Ban' }}
                </button>
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
import Swal from "sweetalert2";

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
    async ban(user) {
      let title = `Ban ${user.username}`;
      let msg = `${user.username} can't login anymore`;
      let action = 'banned';

      if (user.status === 'Banned') {
        title = `Un-ban ${user.username}`;
        msg = `${user.username} will be activated again.`;
        action = 'unbanned';
      }

      const result = await Swal.fire({
        title: title,
        text: msg,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-triangle-exclamation"></i> Yes',
        cancelButtonText: '<i class="fas fa-xmark"></i> Cancel',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-danger",
          cancelButton: "btn btn-success"
        },
        showLoaderOnConfirm: true,
        preConfirm: async () => {
          try {
            const response = await axios.patch(`${process.env.VUE_APP_BACKEND}/ban`, {
              user_id: user.id,
              role: 'user'
            });
            return response.data; 
          } catch (error) {
            if (error.response) {
              Swal.showValidationMessage(`Error: ${error.response.data.message}`);
            } else {
              Swal.showValidationMessage(`Request failed: ${error.message}`);
            }
            throw error;
          }
        }
      });

      if (result.isConfirmed) {
        Swal.fire({
          title: "Success!",
          text: `${user.username} has been successfully ${action}.`,
          icon: "success",
          customClass: {
            title: "h4",
            content: "small",
            confirmButton: "btn btn-success",
          },
          buttonsStyling: false,
        });
        this.fetchData();
      }
    }
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
</style>
