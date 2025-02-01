"use client"

export async function update_data (apiurl, endpoint, set_event, set_loop_status, id) {
    const fetch_data = async () => {
        try {
            const query_parameter = id ? `?eventId=${id}` : ""
            const response = await fetch(`${apiurl}/${endpoint}${query_parameter}`)
            const response_json = await response.json()
            if (response_json.success) {
                set_event(response_json.result)
            } else {
                set_event("error")
                set_loop_status(false)
            }
        } catch ( error ) {
            set_event("error")
            set_loop_status(false)
            console.log(`Error en fetch data\nurl: ${apiurl}\nendpoint: ${endpoint}`)
        }
    }
    fetch_data()
}

export async function update_data_post (endpoint, set_event, set_loop_status) {
    const fetch_data = async () => {
        console.log(`fetcheando datos de: ${endpoint}`)
        try {
            const response = await fetch("/api", {
                method: "post",
                body: JSON.stringify({ event: 2, data: { url: endpoint }})
            })
            const response_json = await response.json()
            if (response_json.success) { 
                set_event(response_json.result)
            } else {
                set_event("error")
                set_loop_status(false)
            }
        } catch ( error ) {
            set_event("error")
            set_loop_status(false)
            console.log(`Error en fetch data\nurl: ${apiurl}\nendpoint: ${endpoint}`)
        }
    }
    fetch_data()
}