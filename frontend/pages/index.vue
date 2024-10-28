<template>
  <div>
    <div class="text-lg mx-5">
      Project Demo URL
    </div>
    <div class="mx-5">
      <a href="http://db8.cse.nd.edu/cse30246/loverboy88/" target="_blank">Homepage link</a>
    </div>
    <div>
      <h1>Posts</h1>
      <ul>
        <li v-for="post in posts" :key="post.id">
          <h2>{{ post.title }}</h2>
          <p>{{ post.content }}</p>
        </li>
      </ul>
    </div>
  </div>

</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      posts: [],
    };
  },
  created() {
    console.log(`API Base URL: ${process.env.BASE_URL}${process.env.VUE_APP_API_PATH}`);
    let that = this;
    try {
      that.$api.get('/posts').then((response) => {
        that.posts = response.data;
      });
    } catch (error) {
      console.error("There was an error fetching posts:", error);
    }
  }

}
</script>
