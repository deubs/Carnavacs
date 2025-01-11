"use client"
import { useEffect, useState } from "react"
import css from "./css.module.css"

const Turnstile = ({ data }) => {
    const ip_array = data.deviceName.split(".")
    const last_number = ip_array[ip_array.length - 1]
    return <div className={css.turnstile}>
        <p>Tango {last_number}</p>
        <p>Ingresos: {data.peopleCount}</p>
    </div>
}

export default function Access_point ({ data }) {

    const [ total_people, set_total_people ] = useState(0)
    const { accessDevices } = data

    useEffect(()=>{
        const sum_people = () => {
            let total = 0
            for (let x of accessDevices) { total += x.peopleCount }
            set_total_people(total)
        }
        sum_people()
    }, [])

    return <div className={css.access_point}>
        <span><h3>Ingreso {data.gateName}</h3> <p className={css.total_people}>Ingresos Totales: {total_people} </p></span>
        <div className={css.turnstile_container}>
            { 
            data && 
            data.accessDevices.map(
            (item, index) => <Turnstile key={index} data={item} />)
            }
        </div>
    </div>
}