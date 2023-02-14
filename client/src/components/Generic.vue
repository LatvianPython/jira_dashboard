<template>
  <RefreshableTickets :api_path="'/api/generic/' + $route.params.filter_id">
    <template slot-scope="{ api_result }">
      <Issues
        v-bind:issues="api_result.issues"
        v-bind:orderBy="'issue'"
      ></Issues>
    </template>
  </RefreshableTickets>
</template>

<script>
import Issues from "./Issues";
import RefreshableTickets from "./RefreshableTickets";

export default {
  name: "Generic",
  components: {Issues, RefreshableTickets}
};
</script>

<style scoped></style>
