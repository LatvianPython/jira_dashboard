<template>
  <div class="jumbotron text-center">
    <img
      :src="'https://imgs.xkcd.com/comics/' + comic.src"
      class="rounded img-fluid float-center mx-auto d-block"
      alt="..."
    />
    <a :href="'https://xkcd.com/' + comic.href + '/'" class="btn">
      <p class="btn btn-secondary">Link to xkcd comic</p>
    </a>
  </div>
</template>

<script>
import _ from "lodash";

export default {
  name: "Comic",
  props: {
    comic: {
      type: Object,
      default: function() {
        return _.sample([
          { href: 303, src: "compiling.png" },
          { href: 844, src: "good_code.png" },
          { href: 1270, src: "functional.png" },
          { href: 1319, src: "automation.png" },
          { href: 1926, src: "bad_code.png" },
          { href: 1513, src: "code_quality.png" },
          { href: 1695, src: "code_quality_2.png" },
          { href: 1833, src: "code_quality_3.png" },
          { href: 2138, src: "wanna_see_the_code.png" }
        ]);
      }
    }
  }
};
</script>

<style scoped></style>
