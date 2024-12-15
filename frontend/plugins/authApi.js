import { defineNuxtPlugin } from '#app'
import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()

  // Create Axios instance
  const api = axios.create({
    baseURL: `${config.public.baseURL}${config.public.apiPath}`,
  })

  // Request interceptor to attach token to headers
  api.interceptors.request.use((request) => {
    const token = localStorage.getItem('token') // Replace with a more secure storage option if needed
    if (token) {
      request.headers.Authorization = `Bearer ${token}`
    }
    return request
  }, (error) => {
    return Promise.reject(error)
  })

  // Response interceptor to handle errors or refresh token logic
  api.interceptors.response.use((response) => {
    return response
  }, (error) => {
    // Optional: Handle token expiration logic or general errors
    if (error.response?.status === 401) {
      // Clear token if unauthorized
      localStorage.removeItem('token')
      // Redirect to login or show an alert
      console.error('Unauthorized. Please login again.')
    }
    return Promise.reject(error)
  })

  // Inject into Nuxt app for global use
  nuxtApp.provide('authApi', api)
})
