"use client"

import { useState, useEffect, useRef } from "react"
import { connectChatWebSocket } from "@/libs/api" // Assuming api.js is in libs
import MessageInput from "@/components/forms/message-input" // Reusing your component

export default function WebSocketChatPage() {
  const [messages, setMessages] = useState([])
  const [clientId, setClientId] = useState(null)
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef(null)
  const wsConnectionRef = useRef(null) // To store the WebSocket connection object

  // Initialize client ID from localStorage or generate a new one
  useEffect(() => {
    let storedClientId = localStorage.getItem("chat_client_id")
    if (!storedClientId) {
      storedClientId = crypto.randomUUID()
      localStorage.setItem("chat_client_id", storedClientId)
    }
    setClientId(storedClientId)
  }, [])

  // WebSocket connection logic
  useEffect(() => {
    if (!clientId) return

    console.log("Establishing WebSocket connection for client:", clientId)

    const onMessage = (eventData) => {
      console.log("Received WebSocket message:", eventData)
      // Your Django consumer sends messages with type 'message' and data field
      if (eventData.type === "message" && eventData.data) {
        setMessages((prevMessages) => {
          // Prevent duplicates and sort by timestamp
          const newMessage = eventData.data
          const isDuplicate = prevMessages.some((msg) => msg.id === newMessage.id)
          if (!isDuplicate) {
            return [...prevMessages, newMessage].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
          }
          return prevMessages
        })
      } else if (eventData.type === "connection_established") {
        console.log(eventData.message)
      }
    }

    const onClose = (event) => {
      console.warn("WebSocket connection closed:", event.code, event.reason)
      // Implement reconnection logic here if desired
    }

    const onError = (error) => {
      console.error("WebSocket error:", error)
    }

    // Establish the WebSocket connection
    wsConnectionRef.current = connectChatWebSocket(clientId, onMessage, onClose, onError)

    // Cleanup function: close the WebSocket connection when the component unmounts
    return () => {
      if (wsConnectionRef.current) {
        console.log("Closing WebSocket connection.")
        wsConnectionRef.current.close()
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
    if (!wsConnectionRef.current || wsConnectionRef.current.ws.readyState !== WebSocket.OPEN) {
      console.error("WebSocket connection not open.")
      alert("WebSocket connection not open. Please wait or refresh.")
      return
    }

    setIsSending(true)
    // Send message directly via WebSocket
    wsConnectionRef.current.sendJson({
      type: "message",
      content: content,
    })
    setIsSending(false)
    // No need to optimistically add message here; WebSocket will deliver it back
  }

  return (
    <div className="chat-container">
      <h1>WebSocket Chat</h1>
      <div className="messages-list">
        {messages.length === 0 && <p className="no-messages">No messages yet. Start chatting!</p>}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message-bubble ${msg.client_id === clientId ? "my-message" : "other-message"}`}
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
