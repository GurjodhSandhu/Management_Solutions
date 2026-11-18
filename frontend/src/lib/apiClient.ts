const BASE_URL = import.meta.env.VITE_BASE_URL
const TOKEN = import.meta.env.VITE_TOKEN

interface RequestOptions {
    method?: 'GET' | 'POST' | 'PATCH' | 'DELETE'
    body?: object
}

export async function apiClient<T>(
    path: string,
    options: RequestOptions = {},
): Promise<T>{
    const headers: Record<string, string> = {

        Authorization: `Bearer ${TOKEN}`,
    }
    if (options.body !== undefined) {
        headers['Content-Type'] = 'application/json'
    }
    const res = await fetch(`${BASE_URL}${path}`, {
        method: options.method ?? 'GET',
        headers,
        body: options.body !== undefined ? JSON.stringify(options.body) : undefined
    })
    if (!res.ok) {
    const errorData = await res.json()
    throw new Error(JSON.stringify(errorData))
}
    if (res.status == 204){
        return undefined as T
    }
    return res.json()
}