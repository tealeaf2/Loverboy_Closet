import { defineNuxtPlugin } from '#app'
import axios from 'axios'

export default defineNuxtPlugin(nuxtApp => {
  const config = useRuntimeConfig()
  const api = axios.create({
    baseURL: `${config.public.baseURL}${config.public.apiPath}`,
  })
  nuxtApp.provide('api', api)
});