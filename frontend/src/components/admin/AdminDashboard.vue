<template>
  <AdminLayout>
    <div class="container-fl">
      <h3 class="text-primary my-3">Hello, Admin!</h3>
      <p v-if="items && items.length === 0">No data available.</p>
      <div v-else class="card p-3">
        <h5 class="text-primary my-3">Waiting for approval</h5>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Profile</th>
              <th>Name</th>
              <th>Bio</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="(item, index) in items" :key="index">
              <td>
                <img
                  :src="item.logo"
                  style="width: 45px; height: 45px"
                  class="rounded-circle"
                  />
              </td>
              <td>{{ item.username }}</td>
              <td>{{ item.bio }}</td>
              <td>
                <button 
                  v-on:click="approve(item)" 
                  class="btn btn-sm d-inline me-2 btn-success">
                  <i class=" fas fa-circle-check"></i> 
                  Approve
                </button>
                <button 
                  v-on:click="reject(item)" 
                  class="btn btn-sm d-inline me-2 btn-danger">
                  <i class=" fas fa-ban"></i> 
                  Reject
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
import AdminLayout from "@/views/AdminLayout.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "AdminDashboard",
  components: {
    AdminLayout
  },
  data() {
    return {
      items: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/eo-requested`);
        this.items = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error("Error fetching data:", error);
        this.items = [];
      }
    },
    async approve(user) {
      let title = `Activate ${user.username}`;
      let msg = `${user.username} will be activated.`;
      let action = 'activated';

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
            response = await axios.patch(`${process.env.VUE_APP_BACKEND}/eo-approve`, {
              id: user.id,
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
    async reject(user) {
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
          text: `${user.username} is rejected successfully.`,
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
