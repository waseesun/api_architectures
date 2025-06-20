"use client"

import { useState, useEffect, useRef } from "react"
import { sendMessageAction, pollMessageAction } from "@/actions/pollingActions"
import MessageInput from "@/components/forms/message-input"

export default function LongPollingPage() {
  const [messages, setMessages] = useState([])
  const [clientId, setClientId] = useState(null)
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef(null)
  const isPollingRef = useRef(false) // To prevent multiple polling loops

  // Initialize client ID from localStorage or generate a new one
  useEffect(() => {
    let storedClientId = localStorage.getItem("chat_client_id")
    if (!storedClientId) {
      storedClientId = crypto.randomUUID()
      localStorage.setItem("chat_client_id", storedClientId)
    }
    setClientId(storedClientId)
  }, [])

  // Long polling logic
  useEffect(() => {
    if (!clientId || isPollingRef.current) return

    const longPoll = async () => {
      isPollingRef.current = true
      console.log("Long polling for messages...")
      try {
        const response = await pollMessageAction(clientId, "long")
        if (response && !response.error) {
          setMessages((prevMessages) => {
            const newMessages = response.filter(
              (newMessage) => !prevMessages.some((oldMessage) => oldMessage.id === newMessage.id),
            )
            return [...prevMessages, ...newMessages].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
          })
        } else {
          console.error("Error fetching messages:", response?.error)
        }
      } catch (error) {
        console.error("Long polling failed:", error)
      } finally {
        // Immediately send another request after receiving a response (or error)
        isPollingRef.current = false
        longPoll()
      }
    }

    longPoll() // Start the long polling loop

    // No cleanup needed for interval, as it's a recursive call
    // However, if the component unmounts, the `longPoll` function might still try to update state.
    // A ref can be used to track if the component is mounted.
    let isMounted = true
    return () => {
      isMounted = false
      // No explicit way to cancel ongoing fetch, but prevent state updates
    }
  }, [clientId])

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
    const response = await sendMessageAction(data)
    if (response && !response.error) {
      // Optionally add the sent message to the list immediately
      // The next poll will also pick it up, but this provides instant feedback
      setMessages((prevMessages) => {
        const newMessage = { ...response, client: { client_id: clientId } } // Add client info for display
        return [...prevMessages, newMessage].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
      })
    } else {
      console.error("Error sending message:", response?.error)
      alert(`Failed to send message: ${response?.error}`)
    }
    setIsSending(false)
  }

  return (
    <div className="chat-container">
      <h1>Long Polling Chat</h1>
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
