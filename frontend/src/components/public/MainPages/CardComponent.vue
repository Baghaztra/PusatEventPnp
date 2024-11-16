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
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardComponent",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { weekday: "long", day: "2-digit", month: "long", year: "numeric" };
      return new Intl.DateTimeFormat("id-ID", options).format(new Date(dateString));
    },
    truncateText(text, maxLength) {
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + "...";
      }
      return text;
    },
  },
};
</script>

<style></style>
