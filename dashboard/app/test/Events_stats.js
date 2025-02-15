"use client"

import css from "@/app/styles/events_stats.module.css"
import { store_events_stats } from "@/app/stores/events_stats"

import { Error } from "@/app/components/common/error"
import { Loading } from "@/app/components/common/loading"

export default function Event_stats () {

    const { events_stats } = store_events_stats()

    return <>
    {
        events_stats == "loading" ? <Loading /> :
        events_stats == "error" ? <Error /> :
        <div className={css.main}>
            
        </div>
    }
    </>
}
