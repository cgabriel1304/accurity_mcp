import { v4 as uuidv4 } from 'uuid'

const STORAGE_KEY = 'accurity_conversation_id'

export function getOrCreateConversationId() {
  let id = localStorage.getItem(STORAGE_KEY)
  if (!id) {
    id = uuidv4()
    localStorage.setItem(STORAGE_KEY, id)
  }
  return id
}

export function createNewConversationId() {
  const id = uuidv4()
  localStorage.setItem(STORAGE_KEY, id)
  return id
}
