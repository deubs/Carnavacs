"use client"
import css from "./css.module.css"
import Navbar from "../navbar/navbar"

import Event_stats from "./events_stats/events_stats"

import Sector_stats from "./sector_stats/sector_stats"
import Access_points from "./access_points/access_points"

import { store_dashboard } from "@/app/stores/dashboard"

const Home = () => {
  return <>
  <Event_stats />
  <Access_points />
  </>
}

export default function Dashboard () {
  const { dashboard } = store_dashboard()

    return <div className={css.main}>
      <Navbar /> 
      {
        dashboard == "home" ? <Home /> :
        dashboard == "sector_stats" ? <Sector_stats /> :
        "Error"
      }
      </div>
}
 