"use client"
import { store_notification } from "../stores/notification"
import { useEffect, useState } from "react"

export async function update_data (endpoint) {
    try {
        const response = await fetch(`http://api.carnavaldelpais.com.ar/${endpoint}`)
        /*const response = await fetch(`/api`, {
            method: "post",
            body: JSON.stringify({ event: 2, data: { url: endpoint }})
        })*/
        
        const response_json = await response.json()
        if (response_json.success) return ({ result: response_json.result})
    } catch ( error ) {
        return ({ error: endpoint })
    }
}