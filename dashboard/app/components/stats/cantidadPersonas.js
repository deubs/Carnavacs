"use client"
import css from "./css.module.css"

import { useEffect, useState } from "react"
import { storeTickets } from "@/app/state/state"


const Row = ({ time, people, percent }) => {
    const [ p, sp ] = useState(0)
    useEffect(()=>{
        setTimeout(()=>{
            sp(percent)
        },750)
    },[percent])

    return <div className={css.row}>
        <p>{ time }</p>
        <div className={css.containerBarra}>
        <div className={`${css.barra}`} style={{"width": `${p}%` }}></div>
        </div>
        <p>{ people }</p>
    </div>
}

const CantidadPersonas = () => {
    const [ values, setValues ] = useState()
    const { ingresosPorHora } = storeTickets()

    const toggleValues = () => {
        
        if(Object.keys(ingresosPorHora).length > 1){
            let valores = [];
            const horas = Object.keys(ingresosPorHora)
            const gente = Object.values(ingresosPorHora)
            const unidad = (gente.reduce((max, num)=>Math.max(max, num))) / 100
            
            for(let i = 0; i < horas.length; i++){
                const x = Object.values(ingresosPorHora)[i]
                let unidades = x / unidad
                // lo que contiene el array
                valores.push([horas[i], gente[i], unidades])
            }
            setValues(valores)
        }
    }


    useEffect(()=>{
        toggleValues()
    },[ingresosPorHora])

    return <div className={css.container}>
        <p className={css.subtitulo}>Ingreso de personas por horario</p>
        { values && values.map((item, index)=><Row key={index} time={item[0]} people={item[1]} percent={item[2]} />)}
    </div>
}

export {
    CantidadPersonas
}