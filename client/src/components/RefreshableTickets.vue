<template>
  <div>
    <div class="alert alert-secondary" role="alert">
      <h3>
        <button
          :disabled="is_disabled"
          type="button"
          class="btn btn-secondary btn-lg"
          v-on:click="getIssues()"
        >
          Refresh</button
        >Last refresh: {{ refresh_in }}
      </h3>
    </div>

    <slot :api_result="api_result"></slot>
  </div>
</template>

<script>
import moment from "moment";
import axios from "axios";

export default {
  name: "RefreshableTickets",
  props: {
    api_path: String
  },
  data: function() {
    return {
      api_result: [],
      refresh_interval: 1000 * 180,
      date: moment.duration(0, "seconds")
    };
  },
  computed: {
    is_disabled: function() {
      if (this.date.asSeconds() === 0) {
        return "disabled";
      }
      return undefined;
    },
    refresh_in: function() {
      return this.date.humanize(true);
    }
  },
  created() {
    this.date = moment.duration(0, "milliseconds");
    this.t = setInterval(() => {
      this.date = this.date.subtract(1, "second");
      if (Math.abs(this.date.asMilliseconds()) >= this.refresh_interval) {
        this.getIssues();
      }
    }, 1000);
  },
  destroyed() {
    clearInterval(this.t);
  },
  methods: {
    getIssues: function() {
      axios
        .get(this.api_path, {
          headers: {
            Authorization: "JWT " + this.$localStorage.token
          }
        })
        .then(response => (this.api_result = response.data));
      this.date = moment.duration(0, "milliseconds");
    }
  },
  mounted() {
    this.getIssues();
  },
  watch: {
    api_path: function() {
      this.getIssues();
    }
  }
};
</script>

<style scoped></style>
