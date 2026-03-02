import { useChat } from '../hooks/useChat'
import ChatWindow from '../components/ChatWindow'
import InputBar from '../components/InputBar'
import styles from './ChatPage.module.css'

export default function ChatPage() {
  const { messages, isLoading, activeTools, sendMessage, startNewConversation } = useChat()

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.headerLeft}>
          <span className={styles.logo}>⬡</span>
          <span className={styles.title}>Accurity Assistant</span>
        </div>
        <button className={styles.newChatBtn} onClick={startNewConversation}>
          + New Chat
        </button>
      </header>

      <main className={styles.main}>
        <ChatWindow messages={messages} activeTools={activeTools} />
      </main>

      <footer className={styles.footer}>
        <InputBar onSend={sendMessage} disabled={isLoading} />
      </footer>
    </div>
  )
}
