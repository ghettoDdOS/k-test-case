class LRUCache<T = unknown> {
  private maxSize: number
  data: Map<PropertyKey, T>

  constructor(maxSize: number) {
    this.maxSize = maxSize
    this.data = new Map<PropertyKey, T>()
  }

  get(key: PropertyKey) {
    return this.hit(key)
  }

  set(key: PropertyKey, value: T) {
    if (this.data.size >= this.maxSize && !this.data.has(key)) {
      const first = this.data.keys().next().value!
      this.data.delete(first)
    }

    this.data.delete(key)
    this.data.set(key, value)
  }

  has(key: PropertyKey) {
    const exist = this.data.has(key)
    if (exist)
      this.hit(key)
    return exist
  }

  private hit(key: PropertyKey) {
    const value = this.data.get(key)

    if (value !== undefined) {
      this.data.delete(key)
      this.data.set(key, value)
    }

    return value
  }
}

export { LRUCache }
