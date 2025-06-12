"use client"

import ModalBase from "./modal-base"
import styles from "./delete-confirmation-modal.module.css"

export default function DeleteConfirmationModal({ isOpen, onClose, onConfirm, isSubmitting }) {
  return (
    <ModalBase isOpen={isOpen} onClose={onClose} title="Confirm Deletion">
      <p className={styles.message}>Are you sure you want to delete this product? This action cannot be undone.</p>
      <div className={styles.actions}>
        <button onClick={onConfirm} className={styles.deleteButton} disabled={isSubmitting}>
          {isSubmitting ? "Deleting..." : "Yes, Delete"}
        </button>
        <button onClick={onClose} className={styles.cancelButton} disabled={isSubmitting}>
          No, Cancel
        </button>
      </div>
    </ModalBase>
  )
}
