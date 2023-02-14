<template>
  <div class="descriptor">
    <label>{{ label }}</label>
    <div>{{ data }}</div>
  </div>
</template>

<script>
export default {
  name: "Descriptor",
  props: { label: String, data: String }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
td {
  white-space: pre;
}

.descriptor {
  position: relative;
  display: inline-block;
  float: left;
  width: 8.75em;
  margin-left: 0.5em;
  margin-bottom: 0.8em;
}

.descriptor label {
  font-size: 1.1em;
  color: gray;
}
</style>
