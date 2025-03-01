"use client"

export async function update_data (apiurl, endpoint, set_event, id) {
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
            }
        } catch ( error ) {
            set_event("error")
            console.log(`Error en fetch data\nurl: ${apiurl}\nendpoint: ${endpoint}`)
        }
    }
    return await fetch_data()
}

export async function update_data_post (endpoint, set_event) {
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
            }
        } catch ( error ) {
            set_event("error")
            console.log(`Error en fetch data\nurl: ${apiurl}\nendpoint: ${endpoint}`)
        }
    }
    return await fetch_data()
}


export async function get_total_tickets (apiurl, id) {
    const fetch_data = async () => {
        try {
            const response = await fetch(`${apiurl}/events/stats?eventId=${id}`)
            const response_json = await response.json()
            if (response_json.success) {
                return ({ error: false, quantity: response_json.result.totalTickets })
            } else {
                throw new Error()
            }
        } catch ( error ) {
            console.log(`Error en update_data_nights, get_total_tickets, ${apiurl}, ${id}, Error:\n${error}`)
            return ({ error: true, quantity: false })
        }
    }
    return await fetch_data()
}
