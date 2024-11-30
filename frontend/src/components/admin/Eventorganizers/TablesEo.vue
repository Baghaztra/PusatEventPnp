<template>
  <AdminLayout>
    <div class="container-fl">
      <p v-if="items && items.length === 0">Data tidak tersedia atau sedang dimuat...</p>
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
                <router-link :to="'/organizer/'+item.id" class="btn btn-sm btn-info d-inline me-2"><i class="fas fa-external-link-alt"></i> See</router-link>
                <button 
                  v-on:click="ban(item)" 
                  :class="{
                    'btn btn-sm d-inline me-2': true,
                    'btn-danger' : item.status == 'Active',
                    'btn-success' : item.status != 'Active'
                }">
                  <i :class="{
                    'fas': true,
                    'fa-ban' : item.status == 'Active',
                    'fa-circle-check' : item.status != 'Active'
                  }"></i> 
                  {{ item.status == 'Active'? 'Ban':'Activate' }}
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
  name: "AdminEventorganizers",
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
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/event_organizers`);
        this.items = Array.isArray(response.data) ? response.data : [];
        // console.log("Data fetched:", this.items);
      } catch (error) {
        console.error("Error fetching data:", error);
        this.items = [];
      }
    },
    async ban(user) {
      let title = `Activate ${user.username}`;
      let msg = `${user.username} will be activated.`;
      let action = 'activated';
      
      if (user.status == 'Active') {
        title = `Ban ${user.username}`;
        msg = `${user.username} can't login anymore`;
        action = 'banned';
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
            var response;
            if (user.status == "Waiting Admin") {
              response = await axios.patch(`${process.env.VUE_APP_BACKEND}/eo-approve`, {
                id: user.id,
              });
            }else{
              response = await axios.patch(`${process.env.VUE_APP_BACKEND}/ban`, {
                user_id: user.id,
                role: 'event organizer'
              });
            }
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
    async deleteUser(user) {
      let title = `Reject ${user.username}`;
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
          cancelButton: "btn btn-success"
        },
        showLoaderOnConfirm: true,
        preConfirm: async () => {
          try {
            var response;
            response = await axios.delete(`${process.env.VUE_APP_BACKEND}/event_organizers?id=${user.id}`);
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

<style></style>
