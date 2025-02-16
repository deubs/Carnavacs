"use client"
import styles from "@/app/styles/tickets_data.module.css"
import { store_events_stats } from "@/app/stores/events_stats"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

import Card from "@/app/components/common/Card"
import Event_data from "@/app/components/card-event-stats/components/event_data"
import Tickets_quantity from "@/app/components/card-event-stats/components/tickets_quantity"
import Chart from "@/app/components/card-event-stats/components/chart"

export default function Tickets_data () {
    const { events_stats } = store_events_stats() 
    return <Card>
        <h3>ESTADÍSTICAS DEL EVENTO</h3>
        {
            events_stats == "loading" ? <Loading /> :
            events_stats == "error" ? <Error /> :
            <div className={styles.main}>
                <Event_data />
                <Tickets_quantity />
            </div>
        }
        <Chart />
    </Card>
}
