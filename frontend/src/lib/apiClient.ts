const BASE_URL = import.meta.env.VITE_BASE_URL

// DEV ONLY: anything in VITE_* is compiled into the public bundle.
// Keeping the lookup in one function means that when you build a real login
// flow (token in memory + refresh on 401), this is the only place that changes.
function getAccessToken(): string | undefined {
  return import.meta.env.VITE_TOKEN
}

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PATCH' | 'DELETE'
  body?: object
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

/**
 * Turns whatever the server sent into one readable sentence.
 * Your backend can answer in three shapes:
 *   1. DRF field errors:        { vin: ["Ensure this field has ..."] }
 *   2. DRF detail errors:       { detail: "Authentication credentials ..." }
 *   3. Your custom handler:     { error: { code, messages | message | detail } }
 */
function extractMessage(status: number, body: unknown): string {
  if (status === 0) {
    return "Can't reach the server. Check your connection and try again."
  }

  if (isRecord(body)) {
    if (typeof body.detail === 'string') return body.detail

    if (isRecord(body.error)) {
      const { messages, message } = body.error
      if (Array.isArray(messages)) return messages.map(String).join(' ')
      if (typeof message === 'string') return message
    }
  }

  if (status === 400) return 'Some fields are invalid.'
  if (status === 401) return 'You are not signed in.'
  if (status === 403) return 'You do not have permission to do that.'
  if (status === 404) return 'That item no longer exists.'
  if (status === 429) return 'Too many requests. Wait a moment and try again.'
  if (status >= 500) return 'The server had a problem. Try again later.'
  return 'The request failed.'
}

export class ApiError extends Error {
  readonly status: number
  readonly body: unknown

  constructor(status: number, body: unknown) {
    super(extractMessage(status, body))
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }

  /**
   * Per-field messages from a 400, e.g. { vin: "Ensure this field has ..." }.
   * Empty object when the error isn't about specific fields.
   */
  get fieldErrors(): Record<string, string> {
    const result: Record<string, string> = {}
    if (this.status !== 400 || !isRecord(this.body)) return result

    // Field errors can sit at the top level (DRF serializer) or under error.detail (your handler).
    const source =
      isRecord(this.body.error) && isRecord(this.body.error.detail)
        ? this.body.error.detail
        : this.body

    for (const [key, value] of Object.entries(source)) {
      if (key === 'detail' || key === 'error') continue
      if (Array.isArray(value)) result[key] = value.map(String).join(' ')
      else if (typeof value === 'string') result[key] = value
    }
    return result
  }
}

// Error bodies aren't always JSON (a proxy 502, a throttle page, an empty 204).
// Read as text first, then try to parse, so a bad body can't crash the error path.
async function readBody(res: Response): Promise<unknown> {
  const text = await res.text()
  if (!text) return undefined
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}

export async function apiClient<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const headers: Record<string, string> = { Accept: 'application/json' }

  const token = getAccessToken()
  if (token) headers.Authorization = `Bearer ${token}`

  if (options.body !== undefined) headers['Content-Type'] = 'application/json'

  let res: Response
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      method: options.method ?? 'GET',
      headers,
      body: options.body !== undefined ? JSON.stringify(options.body) : undefined,
    })
  } catch {
    // fetch only rejects on network failure (offline, CORS, server down)
    throw new ApiError(0, undefined)
  }

  const body = await readBody(res)

  if (!res.ok) {
    // TODO when you add real auth: on 401, refresh the token once and retry.
    throw new ApiError(res.status, body)
  }

  // 204 No Content (e.g. DELETE) has an empty body, so this returns undefined.
  return body as T
}