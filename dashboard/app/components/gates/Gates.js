"use client"
import css from "@/app/styles/gates.module.css"
import { store_events_stats } from "@/app/stores/events_stats"
import Gate from "@/app/components/gates/gate"

export default function Gates () {
    const { loaded, data } = store_events_stats()

    return <div className={css.main}>
        <h3>Ingresos</h3>
        {
            loaded && <div className={css.gates}>
                {
                    data.gates.map((item, index)=><Gate key={`gate${index}`} data={item} />)
                }
                </div>
        }
    </div>
}

