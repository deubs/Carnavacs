"use client"
import css from "@/app/styles/dashboard.module.css"
import Navbar from "../components/navbar/navbar"

import Event_current from "../components/events/Events_current"
import Gates from "../components/gates/Gates"
import Qr_scanner from "../components/utils/qr-scanner"
import Tickets_data from "../components/tickets/Tickets_data"
//import Event_stats from "../components/events/Events_stats"

import { store_dashboard } from "../stores/store_dashboard"

const Home = () => {
  return <> 
  <Event_current />
  <Tickets_data />
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
