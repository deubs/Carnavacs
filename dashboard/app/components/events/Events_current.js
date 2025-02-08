"use client"
import css from "@/app/styles/events_current.module.css"
import { store_events_current } from "@/app/stores/events_current"
import { store_event_id } from "@/app/stores/event_id"
import { store_events_list } from "@/app/stores/events_list"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"
import { data_parse } from "@/app/components/common/data_parse"
import { useEffect } from "react"

export default function Event_current () {
    const { events_current, set_events_current } = store_events_current()
    const { event_id } = store_event_id()
    const { events_list } = store_events_list()

    useEffect(()=>{
        if ( events_list != "loading") {
            const event = events_list.filter(event=>event.id == event_id)[0]
            set_events_current(event)
        }
    }, [event_id])

    return <div className={css.main}>
        <h3>ESTADÍSTICAS DEL EVENTO</h3>
    {
        events_current == "loading" ? <Loading /> :
        events_current == "error" ? <Error /> :
        <>
        <p>{events_current.nombre}</p>
        <p>{data_parse(events_current.fecha)}</p>
        </>
    }
    </div>
}