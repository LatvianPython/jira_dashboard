<template>
  <div class="jumbotron text-center">
    <form class="login_form" @submit.prevent="onSubmit">
      <div class="form-group text-left">
        <label for="login">Username:</label>
        <input
          id="login"
          required
          autofocus
          v-model="username"
          class="form-control"
          type="text"
          placeholder="Username"
        />
      </div>
      <div class="form-group text-left">
        <label for="password">Password:</label>
        <input
          required
          id="password"
          v-model="password"
          class="form-control"
          type="password"
          placeholder="Password"
        />
      </div>

      <button class="btn btn-lg btn-primary btn-block" type="submit">
        Log in
      </button>
      <br>
      <div class="alert alert-danger" role="alert" v-if="error_text">
        {{ error_text }}
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data: function() {
    return {
      username: "",
      password: "",
      error_text: ""
    };
  },
  methods: {
    onSubmit: function() {
      axios
        .post("/api/auth", {
          username: this.username,
          password: this.password
        })
        .then(response => {
          this.$localStorage.token = response.data.access_token;
          if ("redirect" in this.$route.query) {
            this.$router.push(this.$route.query.redirect);
          } else {
            this.$router.push("/");
          }
        })
        .catch(error => {
          this.error_text = error.response.data.description;
        });
    }
  }
};
</script>

<style scoped>
.login_form {
  max-width: 20em;
  margin: 0 auto;
}
</style>
