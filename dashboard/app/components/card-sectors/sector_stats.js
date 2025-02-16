"use client"
import styles from "@/app/styles/events_sector_stats.module.css"
import { store_events_sector_stats } from "@/app/stores/events_sector_stats"

import Side_A from "@/app/components/card-sectors/components/side_a"
import Side_B from "@/app/components/card-sectors/components/side_b"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"
import Card from "../common/Card"

export default function Sector_stats () {
    const { sector_stats } = store_events_sector_stats()

    return <Card>
        <h3>SECTORES</h3>
    {

        sector_stats == "loading" ? <Loading /> :
        sector_stats == "error" ? <Error /> :
        <div className={styles.main}>
            <Side_A />
            <Side_B />
        </div>

    }
    </Card>
}
