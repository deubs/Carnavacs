export const fetch_login = async (user, password, url) => {
    const res = await fetch(url, {
      method: "post",
      body: JSON.stringify({ event: 1, data: { user, password }})
    })
    const response = await res.json()
    return response
}
