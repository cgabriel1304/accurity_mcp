import styles from './MessageBubble.module.css'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const isEmpty = !message.content && message.streaming

  return (
    <div className={`${styles.row} ${isUser ? styles.userRow : styles.assistantRow}`}>
      <div className={`${styles.avatar} ${isUser ? styles.userAvatar : styles.assistantAvatar}`}>
        {isUser ? 'You' : 'AI'}
      </div>
      <div
        className={`${styles.bubble} ${isUser ? styles.userBubble : styles.assistantBubble} ${message.error ? styles.errorBubble : ''}`}
      >
        {isEmpty ? (
          <span className={styles.cursor} />
        ) : (
          <>
            <span style={{ whiteSpace: 'pre-wrap' }}>{message.content}</span>
            {message.streaming && <span className={styles.cursor} />}
          </>
        )}
      </div>
    </div>
  )
}
