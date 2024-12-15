import { defineNuxtRouteMiddleware } from '#app'

export default defineNuxtRouteMiddleware((to, from) => {
  // Ensure this code runs only on the client-side
  if (process.client) {
    const token = localStorage.getItem('token');
    
    if (!token) {
      return navigateTo('/login');
    }
  }
})