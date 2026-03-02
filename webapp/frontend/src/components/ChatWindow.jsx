import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import ToolStatus from './ToolStatus'
import styles from './ChatWindow.module.css'

export default function ChatWindow({ messages, activeTools }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, activeTools])

  const isEmpty = messages.length === 0

  return (
    <div className={styles.window}>
      {isEmpty ? (
        <div className={styles.empty}>
          <div className={styles.emptyIcon}>💬</div>
          <p className={styles.emptyTitle}>Ask about your data catalog</p>
          <p className={styles.emptyHint}>
            Try: <em>"Show me all business terms related to customer"</em>
          </p>
        </div>
      ) : (
        <div className={styles.messages}>
          {messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          <ToolStatus tools={activeTools} />
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  )
}
