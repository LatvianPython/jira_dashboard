<template>
  <RefreshableTickets api_path="/api/maintenance">
    <Issues
      slot-scope="{ api_result }"
      v-bind:issues="api_result.issues"
      v-bind:orderBy="'sla_time'"
    ></Issues>
  </RefreshableTickets>
</template>

<script>
import RefreshableTickets from "./RefreshableTickets";
import Issues from "./Issues";

export default {
  name: "Maintenance",
  components: { Issues, RefreshableTickets }
};
</script>

<style scoped></style>
