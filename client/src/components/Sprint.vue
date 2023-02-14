<template>
  <div class="jumbotron">
    <div id="table">
      <b-table
        striped
        hover
        :items="sprint_raw"
        :fields="fields"
        :sort-by.sync="sortBy"
      >
        <template v-slot:cell(developer)="row">
          <b-form-input v-model="row.item.developer" />
        </template>
        <template v-slot:cell(issue)="row">
          <b-form-input v-model="row.item.issue" />
        </template>
        <template v-slot:cell(priority)="row">
          <b-form-input v-model="row.item.priority" />
        </template>
        <template v-slot:cell(buttons)="row">
          <div>
            <button
              :disabled="is_disabled"
              type="button"
              class="btn btn-success btn-sm"
              v-on:click="addIssue(row.index)"
            >
              ^
            </button>
            <button
              :disabled="is_disabled"
              type="button"
              class="btn btn-success btn-sm"
              v-on:click="addIssue(row.index + 1)"
            >
              v
            </button>
            <button
              :disabled="is_disabled"
              type="button"
              class="btn btn-danger  btn-sm"
              v-on:click="sprint_raw.splice(row.index, 1)"
            >
              x
            </button>
          </div>
        </template>
      </b-table>

      <button
        :disabled="is_disabled"
        type="button"
        class="btn btn-secondary btn-lg"
        v-on:click="postData()"
      >
        Update
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Sprint",
  data: function() {
    return {
      fields: ["developer", "issue", "priority", { key: "buttons", label: "" }],
      sprint_raw: []
    };
  },
  created() {
    axios
      .get("/api/sprint", {
        headers: {
          Authorization: "JWT " + this.$localStorage.token
        }
      })
      .then(response => (this.sprint_raw = response.data));
  },
  methods: {
    postData: function() {
      axios
        .post("/api/sprint", this.sprint_raw, {
          headers: {
            Authorization: "JWT " + this.$localStorage.token
          }
        })
        .then(response => (this.sprint_raw = response.data));
    },
    addIssue: function (index) {
      this.sprint_raw.splice(index, 0, {developer: "", issue: "", priority: ""})
    }
  }
};
</script>

<style scoped>
#table {
  max-width: 720px;
  margin: auto;
}
</style>
