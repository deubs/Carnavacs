"use client"

import css from "@/app/styles/events_stats.module.css"
import { store_events_stats } from "@/app/stores/events_stats"
import { useEffect } from "react"
import Tickets_data from "./tickets_data"

export default function Event_stats () {

    const { loaded, data } = store_events_stats()

    return <>
    {
        loaded && <div className={css.main}>
        <h3>Tickets</h3>
        <Tickets_data />
        </div>
    }
    </>
}
