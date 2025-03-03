export const check_ticket = async (url, decodedText, set_data) => {

    console.log(`
        fetcheando datos desde componente qr a:
        url: ${url}
        decodedText: ${decodedText}
        `)

    try {
        const response = await fetch(`${url}/Ticket/Verify?code=${decodedText}`, {
            method: "post",
            body: JSON.stringify({
                decodedText
            })
        })
        const response_json = await response.json()

        if (response_json.success) {
            set_data({
                m1: response_json.result.m1,
                m2: response_json.result.m2,
                info: ""
            })
            
        } else {
            set_data({
                m1: "",
                m2: "",
                info: "Error en la la respuesta del servidor"
            })
        }

    } catch (error) {
        console.log(`
        Error en la query de enviar qr en hooks/scan_qr
        Error: ${error}
        Error en stringify: ${JSON.stringify(error)}
        `)
    }
}