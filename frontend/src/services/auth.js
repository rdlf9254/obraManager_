import http from './http';

const login = async (email, password) => {
  try {
    const response = await http.post('login/', {
      email,
      password
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
const details = async (id) => {
  try {
    const response = await http.get(`user_details/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export { login, details };
