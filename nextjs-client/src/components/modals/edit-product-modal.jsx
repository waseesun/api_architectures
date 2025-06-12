"use client"

import ModalBase from "./modal-base"
import ProductForm from "@/components/forms/product-form"

export default function EditProductModal({ isOpen, onClose, productData, onSubmit, isSubmitting }) {
  return (
    <ModalBase isOpen={isOpen} onClose={onClose} title={`Edit Product: ${productData?.name || ""}`}>
      <ProductForm initialData={productData} onSubmit={onSubmit} onCancel={onClose} isSubmitting={isSubmitting} />
    </ModalBase>
  )
}
