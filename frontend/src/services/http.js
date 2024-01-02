import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';


const http = axios.create({
  baseURL: 'http://localhost:8000/api/',
  timeout: 10000,
  headers: {'Content-Type': 'application/json'}
});

export default http;
