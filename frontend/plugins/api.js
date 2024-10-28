export default function({$axios}, inject) {
  const api = $axios.create({
    baseURL: 'http://127.0.0.1:5000/api'
  });

  // Inject to context as $api
  inject('api', api);
}