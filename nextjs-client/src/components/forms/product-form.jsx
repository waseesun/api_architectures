"use client"

import { useState, useEffect } from "react"
import styles from "./product-form.module.css"

export default function ProductForm({ initialData = {}, onSubmit, onCancel, isSubmitting }) {
  const [name, setName] = useState(initialData.name || "")
  const [price, setPrice] = useState(initialData.price || "")
  const [stock, setStock] = useState(initialData.stock || "")
  const [errors, setErrors] = useState({})

  useEffect(() => {
    setName(initialData.name || "")
    setPrice(initialData.price || "")
    setStock(initialData.stock || "")
    setErrors({}) // Clear errors when initialData changes
  }, [initialData])

  const validateForm = () => {
    const newErrors = {}
    if (!name.trim()) {
      newErrors.name = "Product name is required."
    }
    if (price === "" || isNaN(price) || Number.parseFloat(price) <= 0) {
      newErrors.price = "Price must be a positive number."
    }
    if (stock === "" || isNaN(stock) || Number.parseInt(stock) < 0) {
      newErrors.stock = "Stock must be a non-negative integer."
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit({ name, price: Number.parseFloat(price), stock: Number.parseInt(stock) })
    }
  }

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <div className={styles.formGroup}>
        <label htmlFor="name" className={styles.label}>
          Product Name:
        </label>
        <input
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className={styles.input}
          disabled={isSubmitting}
        />
        {errors.name && <p className={styles.errorText}>{errors.name}</p>}
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="price" className={styles.label}>
          Price:
        </label>
        <input
          type="number"
          id="price"
          step="0.01"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          className={styles.input}
          disabled={isSubmitting}
        />
        {errors.price && <p className={styles.errorText}>{errors.price}</p>}
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="stock" className={styles.label}>
          Stock:
        </label>
        <input
          type="number"
          id="stock"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          className={styles.input}
          disabled={isSubmitting}
        />
        {errors.stock && <p className={styles.errorText}>{errors.stock}</p>}
      </div>
      <div className={styles.formActions}>
        <button type="submit" className={styles.submitButton} disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : initialData.id ? "Update Product" : "Create Product"}
        </button>
        <button type="button" onClick={onCancel} className={styles.cancelButton} disabled={isSubmitting}>
          Back
        </button>
      </div>
    </form>
  )
}
