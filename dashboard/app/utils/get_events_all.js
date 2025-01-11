export const get_events_all = async () => {
    const res = await fetch(`/api`, {
      method: "post",
      body: JSON.stringify({ event: 4, data: { evento: "events" }})
    })
    const response =  await res.json()
    return response
    }
    