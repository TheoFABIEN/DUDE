export async function uploadZip(file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('http://localhost:8000/upload', {
    method: 'POST',
    body: formData
  })

  return response.json()
}

export async function downloadResults(results) {
  const response = await fetch('http://localhost:8000/download', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(results)
  })

  return await response.blob()
}