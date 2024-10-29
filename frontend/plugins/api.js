export default function({$axios}, inject) {
  const api = $axios.create({
    baseURL: `${process.env.BASE_URL}${process.env.VUE_APP_API_PATH}`
  });

  // Inject to context as $api
  inject('api', api);
}