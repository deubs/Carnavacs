"use client"
import styles from "@/app/styles/dashboard.module.css"

import Navbar from "@/app/components/navbar/navbar"
import Gates from "@/app/components/card-turnstiles/gates"
import Qr_scanner from "@/app/components/card-qr-scan/qr-scanner"
import Tickets_data from "@/app/components/card-event-stats/tickets_data"
import Sector_stats from "@/app/components/card-sectors/sector_stats"
//import Event_stats from "@/app/components/events/Events_stats"

import { store_dashboard } from "@/app/stores/store_dashboard"

export default function Dashboard () {
  const { container } = store_dashboard()

    return <div className={styles.dashboard}>
      <Navbar />

      {
        container == "home" ? 
        <>
        <Tickets_data />
        <Sector_stats />
        <Gates />      
        </> :
        container == "qr_scan" ? 
        <Qr_scanner /> :
        "Error en store_dashboard"
      }
    </div>
}
