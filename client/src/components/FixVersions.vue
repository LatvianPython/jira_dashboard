<template>
  <RefreshableTickets api_path="/api/fix_versions">
    <template slot-scope="{ api_result }">
      <div v-for="fix_version of api_result" v-bind:key="fix_version.id">
        <div class="alert alert-secondary" role="alert">
          <h3>
            Fix Version:
            <a
              :href="
                'https://this.is.a.url.to.jira.com/projects/AYY/versions/' +
                  fix_version.id
              "
              >{{ fix_version.name }}
            </a>
          </h3>
        </div>
        <Issues
          v-bind:issues="fix_version.issues"
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
  name: "FixVersions",
  components: { Issues, RefreshableTickets }
};
</script>

<style scoped></style>
