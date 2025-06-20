"use client"

import { useState } from "react"

export default function MessageInput({ onSendMessage, isLoading }) {
  const [messageContent, setMessageContent] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (messageContent.trim() && onSendMessage) {
      await onSendMessage(messageContent)
      setMessageContent("")
    }
  }

  return (
    <form onSubmit={handleSubmit} className="message-input-form">
      <input
        type="text"
        value={messageContent}
        onChange={(e) => setMessageContent(e.target.value)}
        placeholder="Type your message..."
        className="message-input"
        disabled={isLoading}
      />
      <button type="submit" className="send-button" disabled={isLoading}>
        Send
      </button>
    </form>
  )
}
