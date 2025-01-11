export const get_events_stats = async () => {
    const res = await fetch(`${process.env.get_events_stats}`, {
      method: "get"
    })
    const response =  await res.json()
    return response 
    }
    