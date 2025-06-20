"use client"

import { useState, useEffect, useRef } from "react"
import { sendMessageAction, pollMessageAction } from "@/actions/pollingActions"
import MessageInput from "@/components/forms/message-input"

export default function ShortPollingPage() {
  const [messages, setMessages] = useState([])
  const [clientId, setClientId] = useState(null)
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef(null)

  // Initialize client ID from localStorage or generate a new one
  useEffect(() => {
    let storedClientId = localStorage.getItem("chat_client_id")
    if (!storedClientId) {
      storedClientId = crypto.randomUUID()
      localStorage.setItem("chat_client_id", storedClientId)
    }
    setClientId(storedClientId)
  }, [])

  // Short polling logic
  useEffect(() => {
    if (!clientId) return

    const fetchMessages = async () => {
      console.log("Short polling for messages...")
      const response = await pollMessageAction(clientId, "short")
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
    }

    // Fetch immediately on load
    fetchMessages()

    // Set up interval for short polling every 5 seconds
    const intervalId = setInterval(fetchMessages, 5000)

    // Clean up interval on component unmount
    return () => clearInterval(intervalId)
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
      <h1>Short Polling Chat</h1>
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
