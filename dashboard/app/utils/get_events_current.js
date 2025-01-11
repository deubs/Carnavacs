export const get_event_current = async () => {
  const res = await fetch(`/api`, {
    method: "post",
    body: JSON.stringify({ event: 4, data: { evento: "event_current" }})
  })
  const response =  await res.json()
  return response
  }
  