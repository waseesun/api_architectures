"use client"

import ModalBase from "./modal-base"
import ProductForm from "@/components/forms/product-form"

const EMPTY_PRODUCT_DATA = {}

export default function CreateProductModal({ isOpen, onClose, onSubmit, isSubmitting }) {
  return (
    <ModalBase isOpen={isOpen} onClose={onClose} title="Create New Product">
      <ProductForm
        initialData={EMPTY_PRODUCT_DATA}
        onSubmit={onSubmit}
        onCancel={onClose}
        isSubmitting={isSubmitting}
      />
    </ModalBase>
  )
}
