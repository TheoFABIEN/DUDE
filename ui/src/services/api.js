export const BASE_URL = "/api"

export async function uploadZip(file) {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`${BASE_URL}/upload`, {
    method: 'POST',
    body: formData
  })

  return response.json()
}

export async function downloadResults(results) {
  const response = await fetch(`${BASE_URL}/download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(results)
  })

  return await response.blob()
}