<template>
  <a
    class="issue col-auto"
    :class="issue.color"
    :href="'https://this.is.a.url.to.jira.com/browse/' + issue.issue"
  >
    <div>
      <div v-if="issue.recent" class="recency">{{ issue.recent }}</div>
      <div class="sla_color"></div>
      <div class="header">
        <div class="status">{{ issue.status }}</div>
        <div class="issue_number">
          {{ issue.issue }}
          <div class="emoji">{{ issue.emoji }}</div>
        </div>
        <div class="sla_countdown">{{ issue.sla }}</div>
        <div class="summary">{{ issue.summary }}</div>
      </div>
      <div class="description">
        <Descriptor
          v-for="descriptor of issue.descriptors"
          v-bind:key="descriptor.label"
          :label="descriptor.label"
          :data="descriptor.data"
        />
        <TimeTracking v-if="issue.time_tracking" :data="issue.time_tracking"></TimeTracking>
      </div>
    </div>
  </a>
</template>

<script>
import Descriptor from "./Descriptor";
import TimeTracking from './TimeTracking'

export default {
  name: "Issue",
  components: { TimeTracking, Descriptor },
  props: { issue: Object },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.issue {
  line-height: 1;
  width: 20em;
  height: 15em;
  margin: 1em;
  padding: 0;
  color: #000000;
  background: #eeeeee;
  display: inline-block;
  float: left;
  border-radius: 1em;
  position: relative;
}

a.issue:hover {
  color: #000000 !important;
}

.issue_number .emoji {
  display: inline;
  font-size: 0.85em;
}

.issue .recency {
  position: absolute;
  text-align: center;
  left: -1em;
  top: 0.6em;
  font-weight: 700;
  font-size: 1.1em;
  min-width: 6em;
  transform: rotate(-35deg);
  background-color: deepskyblue;
  color: whitesmoke;
  border-radius: 1em;
  opacity: 0.95;
  padding: 0.1em 0;
}

.issue .header {
  margin-bottom: 0.5em;
  margin-left: 0.5em;
  float: left;
  width: 18em;
}

.issue .header div {
  margin-top: 0.4em;
}

.issue .header .issue_number {
  font-size: 1.9em;
  font-weight: 600;
}

.issue .header .sla_countdown {
  font-size: 1.2em;
  font-weight: 600;
  color: dimgray;
}

.issue.red .header .sla_countdown {
  color: darkred;
}

.issue .header .summary {
  min-height: 3em;
  font-size: 0.8em;
  word-wrap: break-word;
}

.issue .header .status {
  float: right;
  color: grey;
  margin-right: 0.55em;
  font-weight: 600;
  font-size: 0.9em;
  font-style: italic;
  position: absolute;
  text-align: right;
  width: 19.5em;
}

.issue.purple .header .status {
  color: purple;
  font-size: 1.5em;
  width: 11.5em;
}

.issue .description {
  float: right;
  width: 18.5em;
  padding-top: 0.6em;
  border-top: 0.05em;
  border-top-style: solid;
  border-top-color: lightgray;
}

.issue .sla_color {
  width: 1.5em;
  float: left;
  height: 15em;
  border-bottom-left-radius: 1em;
  border-top-left-radius: 1em;
}

.issue.red .sla_color {
  background-color: darkred;
}

.issue.yellow .sla_color {
  background-color: #ffd300;
}

.issue.green .sla_color {
  background-color: green;
}

.issue.purple .sla_color {
  background-color: purple;
}

.issue.grey .sla_color {
  background-color: grey;
}
</style>
