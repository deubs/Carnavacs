"use client"

export async function update_data (endpoint) {
    //const { API_URL } = store_enviroment()
    try {

        const response = await fetch(`http://api.carnavaldelpais.com.ar/${endpoint}`)
        const response_json = await response.json()

        if (response_json.success) return ({ result: response_json.result})
    } catch ( error ) {
        return ({ error: endpoint })
    }
}
/*
export async function load_events () {
    try {

        const response = await fetch(`http://api.carnavaldelpais.com.ar/events`)
        const response_json = await response.json()

        if (response_json.success) return ({ result: response_json.result})
    } catch ( error ) {
        return ({ error: endpoint })
    }
}

export async function load_events_current () {
    try {

        const response = await fetch(`http://api.carnavaldelpais.com.ar/events/current`)
        const response_json = await response.json()

        if (response_json.success) return ({ result: response_json.result})
    } catch ( error ) {
        return ({ error: endpoint })
    }
}

export async function load_events_stats () {
    try {

        const response = await fetch(`http://api.carnavaldelpais.com.ar/events/stats`)
        const response_json = await response.json()

        if (response_json.success) return ({ result: response_json.result})
    } catch ( error ) {
        return ({ error: endpoint })
    }
}
*/
/*const response = await fetch(`/api`, {
            method: "post",
            body: JSON.stringify({ event: 2, data: { url: endpoint }})
        })*/

        //"use client"
//import { store_enviroment } from "../stores/enviroment"
/*
*/