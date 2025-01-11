export const fetch_login = async (user, password) => {
    const res = await fetch("/api", {
      method: "post",
      body: JSON.stringify({ event: 1, data: { user, password }})
    })
    const response =  await res.json()
    return response
    }
    