"use server";
import {
  createProduct,
  deleteProduct,
  getProduct,
  getProducts,
  updateProduct,
} from "@/libs/api";


export const getProductsAction = async () => {
  try {
    const response = await getProducts();
    if (response.error) {
      return { error: response.error };
    }
    return response;
  } catch (error) {
    console.error("Error fetching products:", error);
    return { error: error.message || "Error fetching products" };
  }
};

export const getProductAction = async (id) => {
  try {
    const response = await getProduct(id);
    if (response.error) {
      return { error: response.error };
    }
    return response;
  } catch (error) {
    console.error("Error fetching product:", error);
    return { error: error.message || "Error fetching product" };
  }
};

export const createProductAction = async (data) => {
  try {
    const response = await createProduct(data);
    if (response.error) {
      return { error: response.error };
    }
    return response;
  } catch (error) {
    console.error("Error creating product:", error);
    return { error: error.message || "Error creating product" };
  }
};

export const updateProductAction = async (id, data) => {
  try {
    const response = await updateProduct(id, data);
    if (response.error) {
      return { error: response.error };
    }
    return response;
  } catch (error) {
    console.error("Error updating product:", error);
    return { error: error.message || "Error updating product" };
  }
};

export const deleteProductAction = async (id) => {
  try {
    const response = await deleteProduct(id);
    if (response.error) {
      return { error: response.error };
    }
    return response;
  } catch (error) {
    console.error("Error deleting product:", error);
    return { error: error.message || "Error deleting product" };
  }
};


