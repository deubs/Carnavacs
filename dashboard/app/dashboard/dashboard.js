"use client"
import css from "@/app/styles/dashboard.module.css"
import Navbar from "../components/navbar/navbar"
import { store_dashboard } from "@/app/stores/dashboard"

import Event_current from "../components/events/Events_current"
import Event_stats from "../components/events/Events_stats"
import Gates from "../components/gates/Gates"
import Qr_scanner from "../components/utils/qr-scanner"

//import Test from "../test/page"

const Home = () => {
  return <>
  <Event_current /> 
  <Event_stats />
  <Gates />
  </>
}

export default function Dashboard () {
  const { dashboard } = store_dashboard()

    return <div className={css.main}>
      <Navbar />
      {
        dashboard == "home" ? <Home /> :
        dashboard == "qr_scan" ? <Qr_scanner /> :
        "Error"
      }
      </div>
}