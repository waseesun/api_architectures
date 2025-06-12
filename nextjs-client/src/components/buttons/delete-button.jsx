"use client"

import styles from "./delete-button.module.css"

export default function DeleteButton({ onClick }) {
  return (
    <button onClick={onClick} className={styles.button}>
      Delete
    </button>
  )
}
