"use client"
import css from "./css.module.css"
import { useEffect } from "react"

import { store_message } from "@/app/stores/message"
import { store_events } from "@/app/stores/events"
import { update_data } from "@/app/hooks/update_data"

import Event_data from "../event/event"


export default function Events_all () {

    const { set_message } = store_message()
    const { events_all, set_events_all } = store_events()

    useEffect(()=>{
            const get = async () => {
                const { error, data } = await update_data("http://api.carnavaldelpais.com.ar/events")
                if (error)  set_message(`Error obteniendo datos en el componente event_stats`)
                if (data)   set_events_all(data)
            }
            get()
        },[])
    
    return <div className={css.main}>
        <h3>Siguientes eventos:</h3>
        {   
        events_all && 
        events_all.map((item, index)=><Event_data event={item} key={index} />) 
        }
    </div>
}