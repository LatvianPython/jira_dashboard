<template>
  <RefreshableTickets :api_path="'/api/generic/' + selected">
    <template slot-scope="{ api_result }">
      <div class="alert alert-secondary" role="alert">
        <b-col sm="3">
          <h3>
            <b-form-select
              v-model="selected"
              :options="options"
              value-field="item"
              text-field="name"
              disabled-field="notEnabled"
            ></b-form-select>
          </h3>
        </b-col>
      </div>
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
import axios from "axios";

export default {
  name: "Selectable",
  components: { Issues, RefreshableTickets },
  data: function() {
    return {
      filter_id: "",
      selected: "",
      options: []
    };
  },
  created() {
    axios
      .get("/api/filters", {
        headers: {
          Authorization: "JWT " + this.$localStorage.token
        }
      })
      .then(response => {
        this.options = response.data;
        this.selected = this.options[0].item;
      });
  }
};
</script>

<style scoped></style>
