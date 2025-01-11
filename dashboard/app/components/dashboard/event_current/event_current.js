"use client"
import css from "./css.module.css"

import { store_message } from "@/app/stores/message"
import { store_events } from "@/app/stores/events"
import Event_data from "../event_data/Event_data"
import { update_data } from "@/app/hooks/update_data"

import { useEffect } from "react"


export default function Event_current () {
    
    const { set_message } = store_message()
    const { event_current, set_event_current } = store_events()
    
    useEffect(()=>{

            const get = async () => {
                const { error, data } = await update_data("http://api.carnavaldelpais.com.ar/events/current")
                if (error)  set_message(`Error obteniendo datos en el componente event_stats`)
                if (data) { console.log(data) }
            }
            get()
        },[])

    return <div className={css.main}>
        <h3>Evento siguiente</h3>
        { event_current && <Event_data event={event_current}/> }       
    </div>
}