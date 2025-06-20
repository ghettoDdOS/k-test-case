function formatDateTime(value: Date) {
  return Intl.DateTimeFormat('ru-RU', {
    dateStyle: 'short',
    timeStyle: 'short',
  }).format(value)
}

export { formatDateTime }
