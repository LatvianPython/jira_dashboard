<template>
  <div id="app">
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
      <router-link class="navbar-brand" to="/">Jira Dashboard</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon" />
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/maintenance" v-if="isLoggedIn"
              >Maintenance</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              to="/change_requests"
              v-if="isLoggedIn"
              >Change Requests</router-link
            >
          </li>

<!--          <li class="nav-item">-->
<!--            <router-link class="nav-link" to="/tested" v-if="isLoggedIn"-->
<!--              >Tested</router-link-->
<!--            >-->
<!--          </li>-->

          <li class="nav-item">
            <router-link class="nav-link" to="/fix_versions" v-if="isLoggedIn"
              >Fix Versions</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/sprint" v-if="isAdmin"
              >Sprint</router-link
            >
          </li>

          <li
            class="nav-item"
            v-for="filter of favorite_filters"
            v-bind:key="filter.filter_id"
          >
            <router-link
              class="nav-link"
              :to="'/generic/' + filter.filter_id"
              >{{ filter.name }}</router-link
            >
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/selectable" v-if="isLoggedIn"
              >Selectable</router-link
            >
          </li>
        </ul>

        <ul class="navbar-nav ml-auto">
          <li class="nav-item" v-if="isLoggedIn">
            <router-link
              class="nav-link"
              to="/logoff"
              v-on:click.native="logOff()"
              >Log off</router-link
            >
          </li>
          <li class="nav-item" v-else>
            <router-link class="nav-link" to="/login">Log in</router-link>
          </li>
        </ul>
      </div>
    </nav>

    <router-view />

    <div class="navbar static-bottom  navbar-dark bg-dark">
      <div class="container">
        <p class="navbar-text pull-left">
          Made by
          <a href="https://github.com/LatvianPython">LatvianPython</a> with
          ❤️&🐍
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";
import axios from "axios";

export default {
  name: "app",
  data: function() {
    return {
      favorite_filters: []
    };
  },
  computed: {
    isLoggedIn: function() {
      return this.$localStorage.token && this.$localStorage.token !== "";
    },
    isAdmin: function() {
      if (this.$localStorage.token) {
        return jwt_decode(this.$localStorage.token).is_admin;
      }
      return false;
    }
  },
  created() {
    this.fetchFavoriteFilters();
  },
  watch: {
    isLoggedIn: function() {
      this.fetchFavoriteFilters();
    }
  },
  methods: {
    logOff: function() {
      this.$localStorage.token = undefined;
    },
    fetchFavoriteFilters: function() {
      if (this.isLoggedIn) {
        axios
          .get("/api/favorite_filters", {
            headers: {
              Authorization: "JWT " + this.$localStorage.token
            }
          })
          .then(response => (this.favorite_filters = response.data));
      } else {
        this.favorite_filters = []
      }
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-top: 60px;
}
</style>
