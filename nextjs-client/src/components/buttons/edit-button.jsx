"use client"

import styles from "./edit-button.module.css"

export default function EditButton({ onClick }) {
  return (
    <button onClick={onClick} className={styles.button}>
      Edit
    </button>
  )
}
