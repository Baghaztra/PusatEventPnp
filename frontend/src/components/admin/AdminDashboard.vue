<template>
  <AdminLayout>
    <div class="container-fl">
      <h3 class="text-primary my-3">Hello, Admin!</h3>
      <div v-if="eoWaiting && eoWaiting.length > 0" class="card p-3 mb-3">
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
            <tr v-for="(item, index) in eoWaiting" :key="index">
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
      <div v-if="reports && reports.length > 0" class="card p-3 mb-3">
        <h5 class="text-primary my-3">Newest reports</h5>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Reported</th>
              <th>Reported by</th>
              <th>Message</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="(item, index) in reports" :key="index">
              <td>
                {{ item.reported_type == "eo" ? 'EO':(item.reported_type == "user" ? 'User':'Event') }}
                "{{ item.reported.name }}"
              </td>
              <td>{{ item.reported_by.username }}</td>
              <td>{{ item.message }}</td>
              <td>
                <button 
                  v-on:click="understandReport(item)" 
                  class="btn btn-sm d-inline me-2 btn-success">
                  <i class=" fas fa-circle-check"></i> 
                  Understand
                </button>
                <button 
                  v-on:click="goto(item)" 
                  v-if="item.reported_type != 'user'"
                  class="btn btn-sm d-inline me-2 btn-info">
                  <i class=" fas fa-external-link-alt"></i> 
                  See
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
import router from "@/router";
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
      eoWaiting: [],
      reports: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const requested = await axios.get(`${process.env.VUE_APP_BACKEND}/eo-requested`);
        this.eoWaiting = Array.isArray(requested.data) ? requested.data : [];
      } catch (error) {
        console.error("Error fetching waiting list:", error);
        this.eoWaiting = [];
        this.reports = [];
      }
      try {
        const reported = await axios.get(`${process.env.VUE_APP_BACKEND}/reports`);
        this.reports = Array.isArray(reported.data) ? reported.data : [];
      } catch (error) {
        console.error("Error fetching reports:", error);
        this.reports = [];
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
          confirmButton: "btn btn-success",
          cancelButton: "btn btn-danger"
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
          cancelButton: "btn btn-secondary"
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
    },
    async understandReport(item) {
      let title = `Understand?`;
      let msg = `System assumes you are aware of the report on ${item.reported.name}.
                 We will wipe data of the reports. The final decision is yours.
                 You can manually ban or delete them, or just leave it be.`;

      const result = await Swal.fire({
        title: title,
        text: msg,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-triangle-exclamation"></i> Wipe report data',
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
            response = await axios.delete(`${process.env.VUE_APP_BACKEND}/reports?id=${item.id}`);
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
          text: `Data reports wiped successfully.`,
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
    goto(item){
      if(item.reported_type == 'eo'){
        router.push(`/organizer/${item.reported.id}`)
      }else{
        router.push(`/event/${item.reported.id}`)
      }
    }
  },
  mounted() {
    this.fetchData();
  },
};
</script>
