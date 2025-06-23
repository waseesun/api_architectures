"use client"

import { useState, useEffect, useRef } from "react"
import { streamMessages } from "@/libs/api" // Assuming api.js is in libs
import { sendMessageAction } from "@/actions/pollingActions"
import MessageInput from "@/components/forms/message-input" // Reusing your component

export default function SSEChatPage() {
  const [messages, setMessages] = useState([])
  const [clientId, setClientId] = useState(null)
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef(null)
  const eventSourceRef = useRef(null) // To store the EventSource instance

  // Initialize client ID from localStorage or generate a new one
  useEffect(() => {
    let storedClientId = localStorage.getItem("chat_client_id")
    if (!storedClientId) {
      storedClientId = crypto.randomUUID()
      localStorage.setItem("chat_client_id", storedClientId)
    }
    setClientId(storedClientId)
  }, [])

  // SSE connection logic
  useEffect(() => {
    if (!clientId) return

    console.log("Establishing SSE connection for client:", clientId)

    const onMessage = (newMessage) => {
      console.log("Received SSE message:", newMessage)
      setMessages((prevMessages) => {
        // Prevent duplicates and sort by timestamp
        const isDuplicate = prevMessages.some((msg) => msg.id === newMessage.id)
        if (!isDuplicate) {
          return [...prevMessages, newMessage].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
        }
        return prevMessages
      })
    }

    const onError = (error) => {
      console.error("SSE EventSource error:", error)
      // Handle reconnection logic if needed, EventSource usually retries automatically
    }

    const onOpen = () => {
      console.log("SSE connection opened successfully.")
    }

    // Establish the SSE connection
    eventSourceRef.current = streamMessages(clientId, onMessage, onError, onOpen)

    // Cleanup function: close the EventSource connection when the component unmounts
    return () => {
      if (eventSourceRef.current) {
        console.log("Closing SSE connection.")
        eventSourceRef.current.close()
      }
    }
  }, [clientId]) // Re-run effect if clientId changes

  // Scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async (content) => {
    if (!clientId) {
      console.error("Client ID not available.")
      return
    }
    setIsSending(true)
    const data = { client_id: clientId, content }
    const response = await sendMessageAction(data) // Call the server action
    if (response && response.error) {
      console.error("Error sending message:", response.error)
      alert(`Failed to send message: ${response.error}`)
    }
    // No need to optimistically add message here; SSE will deliver it
    setIsSending(false)
  }

  return (
    <div className="chat-container">
      <h1>SSE Chat</h1>
      <div className="messages-list">
        {messages.length === 0 && <p className="no-messages">No messages yet. Start chatting!</p>}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message-bubble ${msg.client?.client_id === clientId ? "my-message" : "other-message"}`}
          >
            <p className="message-content">{msg.content}</p>
            <span className="message-timestamp">{new Date(msg.timestamp).toLocaleTimeString()}</span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <MessageInput onSendMessage={handleSendMessage} isLoading={isSending} />
    </div>
  )
}
