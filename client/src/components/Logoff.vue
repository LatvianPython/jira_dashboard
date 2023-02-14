<template>
  <Comic :comic="{ href: 1739, src: 'fixing_problems.png' }"></Comic>
</template>

<script>
import Comic from './Comic'

export default {
  name: "Logoff",
  components: { Comic }
};
</script>

<style scoped>
</style>
