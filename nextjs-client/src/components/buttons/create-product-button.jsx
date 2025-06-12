"use client"

import styles from "./create-product-button.module.css"

export default function CreateProductButton({ onClick }) {
  return (
    <button onClick={onClick} className={styles.button}>
      Create Product
    </button>
  )
}
