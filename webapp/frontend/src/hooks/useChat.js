import { useCallback, useEffect, useRef, useState } from 'react'
import { createNewConversationId, getOrCreateConversationId } from '../utils/conversation'

export function useChat() {
  const [conversationId, setConversationId] = useState(() => getOrCreateConversationId())
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [activeTools, setActiveTools] = useState([])
  const abortRef = useRef(null)

  // Load persisted history whenever the conversation changes
  useEffect(() => {
    let cancelled = false
    fetch(`/api/conversations/${conversationId}/messages`)
      .then(r => r.ok ? r.json() : [])
      .then(data => {
        if (!cancelled) {
          setMessages(
            data.map((m, i) => ({ id: `hist-${i}`, role: m.role, content: m.content }))
          )
        }
      })
      .catch(err => { console.error('[useChat] Failed to load conversation history:', err) })
    return () => { cancelled = true }
  }, [conversationId])

  const sendMessage = useCallback(async (text) => {
    const trimmed = text.trim()
    if (!trimmed || isLoading) return

    const userMsg = { id: `u-${Date.now()}`, role: 'user', content: trimmed }
    const asstMsg = { id: `a-${Date.now()}`, role: 'assistant', content: '', streaming: true }
    setMessages(prev => [...prev, userMsg, asstMsg])
    setIsLoading(true)
    setActiveTools([])

    abortRef.current = new AbortController()

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: trimmed, conversation_id: conversationId }),
        signal: abortRef.current.signal,
      })

      if (!res.ok) {
        console.error('[useChat] HTTP error from /api/chat:', res.status, res.statusText)
        throw new Error(`Server error ${res.status}`)
      }

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''  // keep incomplete last line

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          let evt
          try { evt = JSON.parse(line.slice(6)) } catch { continue }
          handleEvent(evt)
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('[useChat] Stream error:', err)
        setMessages(prev => {
          const msgs = [...prev]
          const last = msgs[msgs.length - 1]
          if (last?.streaming) {
            msgs[msgs.length - 1] = {
              ...last,
              content: last.content || `Error: ${err.message}`,
              streaming: false,
            }
          }
          return msgs
        })
      }
    } finally {
      setIsLoading(false)
      setActiveTools([])
      // Ensure last assistant message is no longer marked as streaming
      setMessages(prev => {
        const msgs = [...prev]
        const last = msgs[msgs.length - 1]
        if (last?.streaming) msgs[msgs.length - 1] = { ...last, streaming: false }
        return msgs
      })
    }
  }, [conversationId, isLoading])

  function handleEvent(evt) {
    switch (evt.type) {
      case 'token':
        setMessages(prev => {
          const msgs = [...prev]
          const last = msgs[msgs.length - 1]
          if (last?.streaming) {
            msgs[msgs.length - 1] = { ...last, content: last.content + evt.content }
          }
          return msgs
        })
        break

      case 'tool_start':
        setActiveTools(prev => [...new Set([...prev, evt.tool])])
        break

      case 'tool_end':
        setActiveTools(prev => prev.filter(t => t !== evt.tool))
        break

      case 'done':
        setMessages(prev => {
          const msgs = [...prev]
          const last = msgs[msgs.length - 1]
          if (last?.streaming) msgs[msgs.length - 1] = { ...last, streaming: false }
          return msgs
        })
        break

      case 'error':
        console.error('[useChat] Agent error event:', evt.message)
        setMessages(prev => {
          const msgs = [...prev]
          const last = msgs[msgs.length - 1]
          if (last?.streaming) {
            msgs[msgs.length - 1] = {
              ...last,
              content: last.content || `Error: ${evt.message}`,
              streaming: false,
              error: true,
            }
          }
          return msgs
        })
        break

      default:
        break
    }
  }

  const startNewConversation = useCallback(() => {
    abortRef.current?.abort()
    const newId = createNewConversationId()
    setConversationId(newId)
    setMessages([])
    setIsLoading(false)
    setActiveTools([])
  }, [])

  return {
    conversationId,
    messages,
    isLoading,
    activeTools,
    sendMessage,
    startNewConversation,
  }
}
