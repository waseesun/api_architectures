import { ApiClient } from "./apiClient";


const restApiClient = new ApiClient("http://localhost:8000/django-rest-api");
const realTimeApiClient = new ApiClient("http://localhost:8000/django-real-time-api");

export const getProducts = async () => {
  return await restApiClient.get("/products/");
}

export const getProduct = async (id) => {
  return await restApiClient.get(`/products/${id}/`);
}

export const createProduct = async (data) => {
  return await restApiClient.post("/products/", data);
}

export const updateProduct = async (id, data) => {
  return await restApiClient.patch(`/products/${id}/`, data);
}

export const deleteProduct = async (id) => {
  return await restApiClient.delete(`/products/${id}/`);
}

export const sendMessage = async (data) => {
  return await realTimeApiClient.post("/send-message/", data);
}

export const pollMessage = async (client_id, polling_type) => {
  const queryParams = new URLSearchParams({ client_id, polling_type }).toString();
  return await realTimeApiClient.get(`/poll-messages/?${queryParams}`);
}

export const streamMessages = (client_id, onMessageCallback, onErrorCallback, onOpenCallback) => {
  const queryParams = new URLSearchParams({ client_id }).toString()
  return realTimeApiClient.stream(`/sse-messages/?${queryParams}`, onMessageCallback, onErrorCallback, onOpenCallback)
}