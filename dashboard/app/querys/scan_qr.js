export const check_ticket = async (url, decodedText) => {
    try {
        const response = await fetch(`${url}/Ticket/Verify?code=${code}`, {
            method: "post",
            headers: new Headers({"content-type":"application/json"}),
            body: JSON.stringify({
                decodedText
            })
        })
        const response_json = await response.json()
        if (response_json.success) {
            return response_json
        } else {
            throw "error"
        }
    } catch (error) {
        throw new Error("Error en la query de enviar qr en hooks/scan_qr")
    }
    
}