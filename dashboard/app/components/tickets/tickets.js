"use client"
import { useEffect } from "react"
import css from "./css.module.css"
import { storeTickets, storeNoche } from "@/app/state/state"

const  dataTickets = async () => {
    const r = await fetch("/api", {
        method: "post",
        body: JSON.stringify({ event: 2 })
    })
    const response = await r.json()
    if (response.ok) {
        console.log(response)
        return response
    }
}

const Tickets =  () => {
    const { tickets, setTickets } = storeTickets()
    const { noche } = storeNoche()
    
    useEffect(()=>{
        const fetch = async () => {
            const response = await dataTickets()
            setTickets(response)
        }
        fetch()
    },[])
    
    return <div className={css.main}>
        <h2>Tickets, noche {noche}</h2>
        <div className={css.casillas}>
        <div className={css.casilla}>
        <h4>Vendidos</h4>
        <h1>{tickets.vendidos}</h1>
        </div>
        <div className={css.casilla}>
        <h4>Ingresos</h4>
        <h1>{tickets.ingresos}</h1>
        </div>
        <div className={css.casilla}>
        <h4>Adultos</h4>
        <h1>{tickets.adultos}</h1>
        </div>
        <div className={css.casilla}>
        <h4>Menores</h4>
        <h1>{tickets.menores}</h1>
        </div>
        <div className={css.casilla}>
        <h4>Otros</h4>
        <h1>{tickets.otros}</h1>
        </div>
        </div>
        
    </div>
}

export {
    Tickets
}