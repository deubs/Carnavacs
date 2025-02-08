"use client"
import css from "@/app/styles/tickets_data.module.css"
import { store_events_stats } from "@/app/stores/events_stats"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

import { BarChart } from "@/app/components/charts/Bar_chart"

export default function Tickets_data () {
    const { events_stats } = store_events_stats()

    return <div className={css.main}>
        <h3>ENTRADAS</h3>
        {
            events_stats == "loading" ? <Loading /> :
            events_stats == "error" ? <Error /> :
            <div className={css.container}>
            <span> <p>Total</p> <h2>{ events_stats.totalTickets }</h2> </span>
            <span> <p>Usados</p> <h2>{ events_stats.usedTickets }</h2> </span>
            <span> <p>Restantes</p> <h2>{ events_stats.remainingTickets }</h2> </span>
            </div>

        }
        <BarChart stats={[events_stats.totalTickets, events_stats.usedTickets, events_stats.remainingTickets]} />
    </div>
}
