"use client"
import { useEffect, useState } from "react"
import css from "./css.module.css"
import { storeTickets } from "@/app/state/state"

const Row = ({ type, percent, quantity }) => {
    const [ p, sp ] = useState(0)
    useEffect(()=>{
        setTimeout(()=>{
            sp(percent)
        },750)
    },[percent])

    return <div className={css.row}>
        <p>{ type }</p>
        <div className={css.containerBarra}>
        <div className={`${css.barra}`} style={{"width": `${p}%` }}></div>
        </div>
        <p>{ quantity }</p>
    </div>
}


const TipoTicket = () => {
    const [ values, setValues ] = useState()
    const { tickets } = storeTickets()

    const updateValues = () => {
        const cantidadesDetickets = [ tickets.adultos, tickets.menores, tickets.otros ]
        const unidad = cantidadesDetickets.reduce((max, num)=>Math.max(max, num)) / 100
        const porcentajes = cantidadesDetickets.map(item => item / unidad)
        setValues([
            ["adultos", porcentajes[0], cantidadesDetickets[0]],
            ["menores", porcentajes[1], cantidadesDetickets[1]],
            ["otros", porcentajes[2], cantidadesDetickets[2]]
        ])
    }

    useEffect(()=>{
        updateValues()   
    },[tickets])

   return <div className={css.container}>
        <p className={css.subtitulo}>Tipos de tickets</p>
        { values && values.map((item, index)=><Row key={index} type={item[0]}  percent={item[1]} quantity={item[2]} />)}
    </div>
}

export {
    TipoTicket
}