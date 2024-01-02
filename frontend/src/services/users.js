import http from './http';

const updateUser = async (user, id) => {
  try {
    const response = await http.put(`/usuario/update/`, user);
    return response.data;
  } catch (error) {
    throw error;
  }
};

const createUser = async (user) => {
  try {
    const response = await http.post('usuario/create', user);
    return response.data;
  } catch (error) {
    throw error;
  }
};

const deleteUser = async (id) => {
  try {
    const response = await http.delete(`usuario/delete/`, { data: { id: id } });
    return response.data;
  } catch (error) {
    console.error('Erro ao deletar o usuário:', error);
    throw error;
  }
};


const getUsers = async () => {
  try {
    const response = await http.get('usuario/all/');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export { updateUser, createUser, getUsers, deleteUser };
