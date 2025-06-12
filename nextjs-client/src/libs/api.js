import { ApiClient } from "./apiClient";


const apiClient = new ApiClient("http://localhost:8000");

export const getProducts = async () => {
  return await apiClient.get("/products");
}

export const getProduct = async (id) => {
  return await apiClient.get(`/products/${id}`);
}

export const createProduct = async (data) => {
  return await apiClient.post("/products", data);
}

export const updateProduct = async (id, data) => {
  return await apiClient.patch(`/products/${id}`, data);
}

export const deleteProduct = async (id) => {
  return await apiClient.delete(`/products/${id}`);
}