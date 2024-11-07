// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: [
    '@nuxt/eslint',
  ],
  plugins: [
    '~/plugins/api.js',
    '~/plugins/element-plus.js', 
  ],
  runtimeConfig: {
    public: {
      baseURL: process.env.BASE_URL || 'http://127.0.0.1:5000',
      apiPath: process.env.VUE_APP_API_PATH || '/api'
    }
  },
})