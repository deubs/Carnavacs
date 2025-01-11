export const post_ticket_validate = async ( ticket ) => {
    const res = await fetch(`${process.env.post_ticket_validate}`, {
      method: "post",
      headers: new Headers({"content-type":"application/json"}),
      body: JSON.stringify({  })
    })
    const response =  await res.json()
    return response
    }
    