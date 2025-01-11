export const fetch_tickets = async () => {
    const r = await fetch("/api", {
        method: "post",
        header: new Headers({
            "content-type":"application/json" 
          }),
        body: JSON.stringify({ event: 4,  data: { evento: "events_stats" } })
    })
    const response = await r.json()
    return response
}