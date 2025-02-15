"use client"

export async function update_data (apiurl, endpoint, set_event, set_loop_status, id) {
    const fetch_data = async () => {
        console.log(`fetcheando datos de: ${apiurl}\nendpoint: ${endpoint}`)
        try {
            const query_parameter = id ? `?eventId=${id}` : ""
            const response = await fetch(`${apiurl}/${endpoint}${query_parameter}`)
            const response_json = await response.json()
            if (response_json.success) {
                set_event(response_json.result)
            } else {
                set_event("error")
                set_loop_status()
            }
        } catch ( error ) {
            set_event("error")
            set_loop_status()
            console.log(`Error en fetch data\nurl: ${apiurl}\nendpoint: ${endpoint}`)
        }
    }
    return await fetch_data()
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
                set_loop_status()
            }
        } catch ( error ) {
            set_event("error")
            set_loop_status()
            console.log(`Error en fetch data\nurl: ${apiurl}\nendpoint: ${endpoint}`)
        }
    }
    return await fetch_data()
}


export async function update_data_nights (apiurl, id) {
    const fetch_data = async () => {
        try {
            const query_parameter = id ? `?eventId=${id}` : ""
            const response = await fetch(`${apiurl}/events/stats${query_parameter}`)
            const response_json = await response.json()
            if (response_json.success) {
                return response_json.result.totalTickets
            } else {
                throw new Error()
            }
        } catch ( error ) {
            console.log(`Error en update_data_nights, ${apiurl}, ${id}, Error:\n${error}`)
        }
    }
    return await fetch_data()
}
