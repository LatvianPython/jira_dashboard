<template>
  <div>
    <div class="jumbotron issue_page">
      <div class="row">
        <div class="issues col">
          <Issue
            v-for="issue of orderedIssues"
            v-bind:key="issue.issue"
            :issue="issue"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Issue from "@/components/Issue";
import _ from "lodash";

export default {
  name: "Issues",
  components: {
    Issue
  },
  props: {
    issues: Array,
    orderBy: String
  },
  computed: {
    orderedIssues: function() {
      return _.orderBy(this.issues, this.orderBy, "asc");
    }
  }
};
</script>

<style scoped>
.jumbotron.issue_page {
  background: #ffffff;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
