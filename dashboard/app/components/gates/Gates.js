"use client"
import css from "@/app/styles/gates.module.css"
import { store_events_stats } from "@/app/stores/events_stats"
import Gate from "@/app/components/gates/gate"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

export default function Gates () {
    const { events_stats } = store_events_stats()

    return <div className={css.main}>
        <h3>Ingresos</h3>
        {
            events_stats == "loading" ? <Loading /> :
            events_stats == "error" ? <Error /> :
            <div className={css.gates}>
                {
                    events_stats.gates.map((item, index)=><Gate key={`gate${index}`} data={item} />)
                }
                </div>
        }
    </div>
}

