"use client"
import css from "@/app/styles/tickets_data.module.css"
import { store_events_stats } from "@/app/stores/events_stats"

export default function Tickets_data () {
    const { loaded, data } = store_events_stats()

    return <>
    {
        loaded && <div className={css.main}>
        <span>
            <p>Total</p>
            <h2>{ data.totalTickets }</h2>
        </span>
        <span>
            <p>Usados</p>
            <h2>{ data.usedTickets }</h2>
        </span>
        <span>
            <p>Restantes</p>
            <h2>{ data.remainingTickets }</h2>
        </span>
        </div> 
    }
    </>
}
