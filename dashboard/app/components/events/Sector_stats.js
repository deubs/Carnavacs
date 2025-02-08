"use client"
import css from "@/app/styles/events_sector_stats.module.css"
import { store_events_sector_stats } from "@/app/stores/events_sector_stats"

import Sector_stats_side_A from "./sector_stats_side_A"
import Sector_stats_side_B from "./sector_stats_side_B"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

export default function Sector_stats () {
    const { sector_stats } = store_events_sector_stats()

    return <div className={css.main}>
        <h3>SECTORES</h3>
    {

        sector_stats == "loading" ? <Loading /> :
        sector_stats == "error" ? <Error /> :
        <div className={css.corsodromo_map}>
            <Sector_stats_side_A />
            <Sector_stats_side_B />
        </div>

    }
    </div>
}
