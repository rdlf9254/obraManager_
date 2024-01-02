import http from "./http";

const getAllProjects = async () => {
  try {
    const response = await http.get(`projects/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
const getAllProjectsNames = async () => {
  try {
    const response = await http.get(`projects/names/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
const getMyProjects = async (id) => {
  try {
    const response = await http.get(`projects/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getProjectById = async (projectId) => {
  try {
    const response = await http.get(`project/${projectId}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
const getNamebyId = async (id) => {
  try {
    const response = await http.get(`usuario/name/${id}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

const uploadPhoto = async (data) => {
  try {
    const response = await http.post("uploadphoto/", {
      data,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export {
  getAllProjects,
  getMyProjects,
  getProjectById,
  getNamebyId,
  uploadPhoto,
  getAllProjectsNames,
};
