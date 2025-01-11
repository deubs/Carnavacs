"use client"
import css from "./css.module.css"
import { useEffect, useState } from "react"

import { store_message } from "@/app/stores/message"
import { update_data } from "@/app/hooks/update_data"
import Access_point from "../access_points/access_point"

export default function Access_points () {

    const [ gates, set_gates ] = useState()
    const { set_message } = store_message()

    useEffect(()=>{
        const get = async () => {
            const { error, data } = await update_data("http://api.carnavaldelpais.com.ar/events/stats")
            if (error)  set_message(`Error obteniendo datos en el componente access_points`)
            if (data)   set_gates(data.gates)
        }
        get()
    },[])
    
    return <div>
        { gates && gates.map((item, index) => <Access_point data={ item } key={index + 999} />)}
    </div>
}
 /*       
    useEffect(()=>{
        const m = async () => {
            const r = await fetch("/api", {
                method: "post",
                body: JSON.stringify({ event: 4, data: { evento: "events_stats" }})
            })
            const rr = await r.json()
            console.log(rr.result.gates)
            set_gates(rr.result.gates)
        }
        m()
    }, [])
*/