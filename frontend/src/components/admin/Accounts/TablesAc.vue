<template>
  <AdminLayout>
    <div class="container-fl">
      <p v-if="accounts && accounts.length === 0">Data tidak tersedia atau sedang dimuat...</p>
      <div v-else class="card p-3">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Role</th>
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
                  'text-bg-primary': item.role == 'admin',
                  'text-bg-secondary': item.role != 'admin'
                }">
                  {{ item.role }}
                </span>
              </td>
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
                  v-on:click="admin(item)" 
                  class="btn btn-sm d-inline me-2 btn-warning">
                  <i class=" fas fa-user"></i> 
                  Change role
                </button>
                <button 
                  v-on:click="ban(item)" 
                  :class="{
                    'btn btn-sm d-inline me-2': true,
                    'btn-danger' : item.status != 'Banned',
                    'btn-success' : item.status == 'Banned'
                }">
                  <i class="fas fa-ban"></i> {{ item.status == 'Banned'? 'Activate':'Ban' }}
                </button>
                <button 
                  v-on:click="deleteUser(item)" 
                  class="btn btn-sm d-inline me-2 btn-danger">
                  <i class=" fas fa-trash"></i> 
                  Delete
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
        input: 'text',
        inputPlaceholder: 'Enter a message...',
        inputValue: action == 'banned'? `${user.username} is banned due to our policy` : `${user.username} is no longger banned`,
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-triangle-exclamation"></i> Yes',
        cancelButtonText: '<i class="fas fa-xmark"></i> Cancel',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-primary",
          cancelButton: "btn btn-secondary"
        },
        showLoaderOnConfirm: true,
        preConfirm: async (message) => {
          try {
            const response = await axios.patch(`${process.env.VUE_APP_BACKEND}/ban`, {
              user_id: user.id,
              role: 'user',
              message: message
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
    },
    async admin(user) {
      let title = `Turn ${user.username} into admin?`;
      let action = "Admin"
      
      if (user.role === 'admin') {
        title = `Turn ${user.username} into regular user?`;
        action = "regular user"
      }

      const result = await Swal.fire({
        title: title,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-triangle-exclamation"></i> Yes',
        cancelButtonText: '<i class="fas fa-xmark"></i> Cancel',
        customClass: {
          title: "fs-5 text-primary",
          confirmButton: "btn btn-success",
          cancelButton: "btn btn-secondary"
        },
        showLoaderOnConfirm: true,
        preConfirm: async () => {
          try {
            const response = await axios.patch(`${process.env.VUE_APP_BACKEND}/role-admin`, {
              user_id: user.id,
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
          text: `${user.username} is now ${action}.`,
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
    },
    async deleteUser(user) {
      let title = `Delete account ${user.username}`;
      let msg = `${user.username} will be deleted forever.`;

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
          cancelButton: "btn btn-secondary"
        },
        showLoaderOnConfirm: true,
        preConfirm: async () => {
          try {
            var response;
            response = await axios.delete(`${process.env.VUE_APP_BACKEND}/users?id=${user.id}`);
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
          text: `${user.username} is deleted successfully.`,
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
