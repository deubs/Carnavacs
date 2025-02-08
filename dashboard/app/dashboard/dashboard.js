"use client"
import css from "@/app/styles/dashboard.module.css"

import Navbar from "@/app/components/navbar/navbar"
import Event_current from "@/app/components/events/Events_current"
import Gates from "@/app/components/gates/Gates"
import Qr_scanner from "@/app/components/utils/qr-scanner"
import Tickets_data from "@/app/components/tickets/Tickets_data"
import Sector_stats from "@/app/components/events/Sector_stats"
//import Event_stats from "@/app/components/events/Events_stats"

import { store_dashboard } from "@/app/stores/store_dashboard"

const Home = () => {
  return <> 
  <Event_current />
  <Tickets_data />
  <Sector_stats />
  <Gates />
  </>
}

export default function Dashboard () {
  const { container } = store_dashboard()

    return <div className={css.main}>
      <Navbar />
      {
        container == "home" ? <Home /> :
        container == "qr_scan" ? <Qr_scanner /> :
        "Error"
      }
    </div>
}
