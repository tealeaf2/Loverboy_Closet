import { defineNuxtPlugin } from '#app'
import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const api = axios.create({
    baseURL: `${process.env.BASE_URL}${process.env.VUE_APP_API_PATH}`,
  })
  nuxtApp.provide('api', api)
});