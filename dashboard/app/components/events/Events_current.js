"use client"
import css from "@/app/styles/events_current.module.css"
import { store_events_current } from "@/app/stores/events_current"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"
import { data_parse } from "@/app/components/common/data_parse"

export default function Event_current () {
    const { events_current } = store_events_current()
    
    return <div className={css.main}>
        <h3>Estadísticas del evento</h3>
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