"use client"
import css from "@/app/styles/events_current.module.css"
import { useEffect } from "react"
import { store_events_current } from "@/app/stores/events_current"

export default function Event_current () {
    const { loaded, data } = store_events_current()

    return <div className={css.main}>
        <h3>Evento siguiente</h3>
    {
        loaded && <>
        <p>{data.nombre}</p>
        <p>{data.fecha != "cargando" ? new Date(data.fecha).toLocaleDateString("es-ES", { year: "numeric", month: "long", day: "2-digit"}) : data.fecha }</p>
        </>
    }
    </div>
}