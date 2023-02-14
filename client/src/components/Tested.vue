<template>
  <RefreshableTickets api_path="/api/tested">
    <Issues
      slot-scope="{ api_result }"
      v-bind:issues="api_result.issues"
      v-bind:orderBy="'issue'"
    ></Issues>
  </RefreshableTickets>
</template>

<script>
import RefreshableTickets from "./RefreshableTickets";
import Issues from "./Issues";

export default {
  name: "Tested",
  components: { Issues, RefreshableTickets }
};
</script>

<style scoped></style>
