"use client"

import { useState, useEffect } from "react"
import { getProductsAction, createProductAction, updateProductAction, deleteProductAction } from "@/actions/productActions"
import CreateProductButton from "@/components/buttons/create-product-button"
import EditButton from "@/components/buttons/edit-button"
import DeleteButton from "@/components/buttons/delete-button"
import CreateProductModal from "@/components/modals/create-product-modal"
import EditProductModal from "@/components/modals/edit-product-modal"
import DeleteConfirmationModal from "@/components/modals/delete-confirmation-modal"
import styles from "./page.module.css"

export default function ProductsPage() {
  const [products, setProducts] = useState([])
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [message, setMessage] = useState(null) // { type: 'success' | 'error', text: string }
  const [isSubmitting, setIsSubmitting] = useState(false)

  const fetchProducts = async () => {
    const res = await getProductsAction()
    if (res.error) {
      setMessage({ type: "error", text: res.error })
      setProducts([]) // Clear products on error
    } else {
      setProducts(res)
      setMessage(null) // Clear message on successful fetch
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleCreateProduct = async (data) => {
    setIsSubmitting(true)
    const res = await createProductAction(data)
    if (res.error) {
      setMessage({ type: "error", text: res.error })
    } else {
      setMessage({ type: "success", text: "Product created successfully!" })
      setShowCreateModal(false)
      // fetchProducts will be triggered by revalidatePath in the action
    }
    setIsSubmitting(false)
  }

  const handleUpdateProduct = async (data) => {
    setIsSubmitting(true)
    const res = await updateProductAction(selectedProduct.id, data)
    if (res.error) {
      setMessage({ type: "error", text: res.error })
    } else {
      setMessage({ type: "success", text: "Product updated successfully!" })
      setShowEditModal(false)
      setSelectedProduct(null)
      // fetchProducts will be triggered by revalidatePath in the action
    }
    setIsSubmitting(false)
  }

  const handleDeleteProduct = async () => {
    setIsSubmitting(true)
    const res = await deleteProductAction(selectedProduct.id)
    if (res.error) {
      setMessage({ type: "error", text: res.error })
    } else {
      setMessage({ type: "success", text: "Product deleted successfully!" })
      setShowDeleteModal(false)
      setSelectedProduct(null)
      // fetchProducts will be triggered by revalidatePath in the action
    }
    setIsSubmitting(false)
  }

  const openEditModal = (product) => {
    setSelectedProduct(product)
    setShowEditModal(true)
  }

  const openDeleteModal = (product) => {
    setSelectedProduct(product)
    setShowDeleteModal(true)
  }

  return (
    <main className={styles.container}>
      <h1 className={styles.pageTitle}>Products</h1>
      <div className={styles.header}>
        <CreateProductButton onClick={() => setShowCreateModal(true)} />
        {message && (
          <p className={`${styles.message} ${message.type === "success" ? styles.success : styles.error}`}>
            {message.text}
          </p>
        )}
      </div>

      <div className={styles.productList}>
        {products.length === 0 ? (
          <p className={styles.noProducts}>No products found. Create one!</p>
        ) : (
          products.map((product) => (
            <div key={product.id} className={styles.productCard}>
              <h2 className={styles.productName}>{product.name}</h2>
              <div className={styles.productDetails}>
                <p>Price: ${product.price}</p>
                <p>Stock: {product.stock}</p>
              </div>
              <div className={styles.productActions}>
                <EditButton onClick={() => openEditModal(product)} />
                <DeleteButton onClick={() => openDeleteModal(product)} />
              </div>
            </div>
          ))
        )}
      </div>

      <CreateProductModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSubmit={handleCreateProduct}
        isSubmitting={isSubmitting}
      />

      {selectedProduct && (
        <EditProductModal
          isOpen={showEditModal}
          onClose={() => {
            setShowEditModal(false)
            setSelectedProduct(null)
          }}
          productData={selectedProduct}
          onSubmit={handleUpdateProduct}
          isSubmitting={isSubmitting}
        />
      )}

      {selectedProduct && (
        <DeleteConfirmationModal
          isOpen={showDeleteModal}
          onClose={() => {
            setShowDeleteModal(false)
            setSelectedProduct(null)
          }}
          onConfirm={handleDeleteProduct}
          isSubmitting={isSubmitting}
        />
      )}
    </main>
  )
}
