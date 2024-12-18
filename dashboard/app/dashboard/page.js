"use client"
import css from "./css.module.css"
import { useEffect } from "react"

import { Navbar } from "../components/navbar/navbar"
import { Tickets } from "../components/tickets/tickets"
import { Puertas } from "../components/puertas/puertas"
import { Stats } from "../components/stats/stats"
import Websocket from "../websocket/page"

export default function Dashboard () {
    
    useEffect(()=>{
    },[])

    return <div className={css.main}>
        <Navbar />
        <Websocket />
        <Tickets />
        <Stats />
        <Puertas />
    </div>
} 