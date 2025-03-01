"use client"
import styles from "./page.module.css"

import { store_dashboard } from "@/app/stores/store_dashboard"

import Enviroment from "@/app/components/enviroment/enviroment"
import Loading from "@/app/components/updates/loading/loading"
import Updates from "@/app/components/updates/updates"

import Navbar from "@/app/components/navbar/navbar"
import Gates from "@/app/components/card-turnstiles/gates"
import Tickets_data from "@/app/components/card-event-stats/tickets_data"
import Sector_stats from "@/app/components/card-sectors/sector_stats"
import Qr_scanner from "@/app/components/card-qr-scan/qr-scanner"
import All_nights from "@/app/components/card-all-nights/all-nights"
import Timer from "@/app/components/timer/timer"

export default function Home () {
  const { container } = store_dashboard()

  return <div className={styles.main}> 
    <Enviroment />
    <Updates />  
    <Timer />
    
    {
      container == "loading" ? 
      <Loading /> :
      container == "dashboard" ?
      <>
      <Navbar />
      <All_nights />
      <Tickets_data />
      <Sector_stats />
      <Gates />
      </> :
      container == "qr_scan" ?
      <>
      <Navbar />
      <Qr_scanner />
      </> :
      "Error en el componente Home"
    }

  </div>
}
