// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },

  css: [
    '~/assets/css/base.css'
  ],

  modules: [
    '@nuxt/eslint',
  ],
  components: [
    {
      path: '~/components',
      pathPrefix: true,
    },
  ],
  plugins: [
    '~/plugins/api.js',
    '~/plugins/authApi.js',
    '~/plugins/element-plus.js', 
  ],
  router: {
    middleware: ['auth']
  },
  runtimeConfig: {
    public: {
      baseURL: process.env.BASE_URL || 'http://127.0.0.1:5000',
      apiPath: process.env.VUE_APP_API_PATH || '/api'
    }
  },

  server: {
    host: process.env.HOST || '0.0.0.0',
    port: process.env.PORT || 3000,
  },

  app: {
    baseURL: process.env.BASE_ROUTER || '/'
  },
})