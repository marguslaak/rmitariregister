import axios from 'axios';
import { sendErrorToast } from 'utils/toast';

const baseURL =
  import.meta.env.MODE === 'development'
    ? '/api'
    : import.meta.env.VITE_API_URL || '/';

const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-type': 'application/json',
    Accept: 'application/json',
  },
});

apiClient.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error && error?.response) {
      sendErrorToast({
        content: error?.response?.data?.message ?? 'Tekkis viga',
      });
    }

    return error;
  }
);

export default apiClient;
