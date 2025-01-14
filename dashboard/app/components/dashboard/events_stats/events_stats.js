"use client"
import css from "./css.module.css"

import { useEffect } from "react"
import { store_message } from "@/app/stores/message"
import { store_stats } from "@/app/stores/stats"

import { update_data } from "@/app/hooks/update_data"

export default function Event_stats () {

    const { data, set_data } = store_stats()
    const { set_message } = store_message()

    useEffect(()=>{
        const get = async () => {
            const { error, data } = await update_data("http://api.carnavaldelpais.com.ar/events/stats")
            if (error)  set_message(`Error: compruebe el estado de la conexion a la red`)
            if (data)   set_data(data)
            console.log(data.gates)
            console.log(data.ticketStats)
        }
        get()
    },[])
    
    return <div className={css.main}>
    <h3>Tickets</h3>
    <div className={css.casillas}> 
        <div className={css.casilla}>
            <p>Total</p>
            <h1>{data.totalTickets}</h1>
        </div>

        <div className={css.casilla}>
            <p>Ingresos</p>
            <h1>{data.usedTickets}</h1>
        </div>
    
        <div className={css.casilla}>
            <p>Restantes</p>
            <h1>{data.remainingTickets}</h1>
        </div>
    </div>       
</div>
}

/*

*/