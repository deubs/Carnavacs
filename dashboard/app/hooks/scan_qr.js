export const check_ticket = async (code) => {
    const response = await fetch(`http://api.carnavaldelpais.com.ar/Ticket/Verify?code=${code}`, {
        method: "post",
        headers: new Headers({"content-type":"application/json"}),
        body: JSON.stringify({
            code
        })
    })
    const response_json = await response.json()
    return response_json
}