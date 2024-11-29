<template>
  <AdminLayout>
    <div class="container-fl">
      <p v-if="items.length === 0">Data tidak tersedia atau sedang dimuat...</p>
      <div v-else class="card p-3">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Title</th>
              <th>Event Organizer</th>
              <th>Event Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="(item, index) in items" :key="index">
              <td>{{ item.title }}</td>
              <td>{{ item.eo }}</td>
              <td>
                {{
                  new Intl.DateTimeFormat("en-EN", {
                    weekday: "long",
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                  }).format(new Date(item.event_date))
                }}
              </td>
              <td>
                <router-link :to="'/event/'+item.id" class="btn btn-info btn-sm d-inline me-2"><i class="fas fa-external-link-alt"></i> See</router-link>
                <a v-on:click="takedown(item.id)" class="btn btn-danger btn-sm d-inline me-2"><i class="fas fa-ban"></i> Take down</a>
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
        const response = await axios.get(`${process.env.VUE_APP_BACKEND}/event-latest`);
        this.items = Array.isArray(response.data) ? response.data : [];
        // console.log("Data fetched:", this.items);
      } catch (error) {
        console.error("Error fetching data:", error);
        this.items = [];
      }
    },
    async takedown(id){
      try {
        const result = await Swal.fire({
          title: "Are you sure?",
          text: "This post will gone forever",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Yes, Delete it",
          cancelButtonText: "Cancel",
          customClass: {
            confirmButton: "btn btn-danger me-3",
            cancelButton: "btn btn-success ms-3",
          },
          buttonsStyling: false,
        });
        if (result.isConfirmed) {
          const response = await axios.delete(`${process.env.VUE_APP_BACKEND}/delete/event?id=${id}`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            }
          );
          console.log(response);
          if (response.status == 200) {
            Swal.fire({
              title: "Deleted",
              text: response.data.message,
              icon: "success"
            });
            this.fetchData();
          }
          else {
            Swal.fire({
              title: "Failed",
              text: response.data.message,
              icon: "error"
            });
          }
        }
      } catch (error) {
        console.log("error",error);
        
        Swal.fire({
          title: "Error!",
          text: error,
          icon: "error",
          customClass: {
            popup: "alert alert-danger",
            title: "h4",
            content: "small",
            confirmButton: "btn btn-sm btn-success",
          },
          buttonsStyling: false,
        });
      }
    }
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}
</style>
