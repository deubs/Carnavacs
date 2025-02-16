"use client"
import { store_events_stats } from "@/app/stores/events_stats"
import Gate from "@/app/components/card-turnstiles/components/gate"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"
import Card from "@/app/components/common/Card"


export default function Gates () {
    const { events_stats } = store_events_stats()

    return <Card>
        <h3>ACCESOS MOLINETES</h3>
        {
            events_stats == "loading" ? <Loading /> :
            events_stats == "error" ? <Error /> :
            events_stats.gates.map((item, index)=><Gate key={`gate${index}`} data={item} />)
        }
    </Card>
}
