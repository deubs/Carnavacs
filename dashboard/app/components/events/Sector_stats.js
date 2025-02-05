"use client"
import css from "@/app/styles/events_sector_stats.module.css"
import { store_events_sector_stats } from "@/app/stores/events_sector_stats"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"
import { Sector_stat } from "@/app/components/events/sector_stat"


export default function Sector_stats () {
    const { sector_stats } = store_events_sector_stats()
    return <div className={css.main}>
        <h3>Sectores</h3>
    {

        sector_stats == "loading" ? <Loading /> :
        sector_stats == "error" ? <Error /> :
        sector_stats.map((item,index)=><Sector_stat data={item} key={index} />)

    }
    </div>
}
