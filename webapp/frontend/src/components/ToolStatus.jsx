import styles from './ToolStatus.module.css'

// Convert snake_case tool names to readable labels
function formatTool(toolName) {
  if (toolName.startsWith('search_')) {
    const resource = toolName.replace('search_', '').replace(/_/g, ' ')
    return `Searching ${resource}…`
  }
  if (toolName.startsWith('get_') && toolName.endsWith('_by_id')) {
    const resource = toolName.replace('get_', '').replace('_by_id', '').replace(/_/g, ' ')
    return `Fetching ${resource}…`
  }
  return `${toolName.replace(/_/g, ' ')}…`
}

export default function ToolStatus({ tools }) {
  if (!tools || tools.length === 0) return null

  return (
    <div className={styles.container}>
      {tools.map(tool => (
        <div key={tool} className={styles.pill}>
          <span className={styles.spinner} />
          {formatTool(tool)}
        </div>
      ))}
    </div>
  )
}
