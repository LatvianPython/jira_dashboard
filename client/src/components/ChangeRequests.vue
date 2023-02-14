<template>
  <RefreshableTickets api_path="/api/change_requests">
    <template slot-scope="{ api_result }">
      <div v-for="data of api_result" v-bind:key="data.developer">
        <div class="alert alert-secondary" role="alert">
          <h3>Developer: {{ data.developer }}</h3>
        </div>
        <Issues
          v-bind:issues="data.change_requests"
          v-bind:orderBy="'priority'"
        ></Issues>
      </div>
    </template>
  </RefreshableTickets>
</template>

<script>
import Issues from "./Issues";
import RefreshableTickets from "./RefreshableTickets";

export default {
  name: "ChangeRequests",
  components: { Issues, RefreshableTickets }
};
</script>

<style scoped></style>
