export const check_ticket = async (url, decodedText, set_data) => {
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
            set_data({

                m1: r.result.m1, 
                m2: r.result.m2 
                
            })
        } else {
            set_data({

                m1: "Error en la validación del tiket",
                m2: "Error en la validación del tiket"
            
            })
        }
    } catch (error) {
        console.log("Error en la query de enviar qr en hooks/scan_qr")
    }
    
}