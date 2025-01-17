"use client"
import css from "@/app/styles/dashboard.module.css"
import Navbar from "../components/navbar/navbar"
import { store_dashboard } from "@/app/stores/dashboard"

import Event_current from "../components/events/Events_current"
import Event_stats from "../components/events/Events_stats"
import Gates from "../components/gates/Gates"

import Sector_stats from "./endpoints/events/4_sector_stats/sector_stats"

const Home = () => {
  return <>
  <Access_points />
  <Event_current /> 
  </>
}
/*
{
        dashboard == "home" ? <Home /> :
        dashboard == "sector_stats" ? <Sector_stats /> :
        "Error"
      }
*/
export default function Dashboard () {
  const { dashboard } = store_dashboard()

    return <div className={css.main}>
      <Navbar />
      <Event_current />
      <Event_stats />
      <Gates />
      </div>
}