<template>
  <div class="timetracking">
    <div v-for="(tracking, klass) in data" v-bind:key="klass" class="timetracking_rec">
      <label>{{ tracking.text }}</label>
      <div class="timetracking_bar" :class="klass">
        <div class="left" :style="'width:' + tracking.left + '%;'"></div>
        <div class="right" :style="'width:' + tracking.right + '%;'"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TimeTracking",
  props: { data: Object }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.timetracking {
  position: relative;
  width: 18.5em;
  float: left;
}

.timetracking .timetracking_rec {
  margin-bottom: 0.2em;
  margin-left: 0.5em;
}

.timetracking_bar {
  position: relative;
  float: right;
  width: 10em;
  margin-right: 1em;
}

.timetracking_bar * {
  height: 1em;
  width: 100%;
  display: inline-block;
  background-color: darkgray;
}

.timetracking_bar .left {
  float: left;
}

.timetracking_bar .right {
  float: right;
}

.timetracking_bar.estimated .left {
  background-color: lightblue;
}

.timetracking_bar.remaining .right {
  background-color: darkorange;
}

.timetracking_bar.logged .left {
  background-color: green;
}
</style>
