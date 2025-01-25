"use client"

export async function update_data (endpoint, callback, id) {
    const fetch_data = async () => {
        try {
            const query_parameter = id ? `?eventId=${id}` : ""
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${endpoint}${query_parameter}`)
            const response_json = await response.json()
            if (response_json.success) callback(response_json.result)
        } catch ( error ) {
            callback("error")
        }
    }
    fetch_data()
}

export async function update_data_post (endpoint, callback) {
    const fetch_data = async () => {
        try {
            const response = await fetch("/api", {
                method: "post",
                body: JSON.stringify({ event: 2, data: { url: endpoint }})
            })
            const response_json = await response.json()
            console.log(response_json)
            if (response_json.success) {
                callback(response_json.result)
            } else {
                throw new Error("Error obteniendo datos")
            }
        } catch ( error ) {
            callback("Error obteniendo datos")
        }
    }
    fetch_data()
}
