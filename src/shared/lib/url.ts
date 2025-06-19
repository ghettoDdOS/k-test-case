function joinUrl(base: string, path: string) {
  if (!base.endsWith('/') && !path.startsWith('/')) {
    return `${base}/${path}`
  }
  if (base.endsWith('/') && path.startsWith('/')) {
    return base + path.slice(1)
  }
  return base + path
}

export { joinUrl }
