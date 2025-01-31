"use client"
import css from "@/app/styles/gate.module.css"
import Turnstile from "./turnstile"

export default function Gate ({ data }) {

    const suma = data.accessDevices.reduce((suma, item)=>suma + item.peopleCount, 0)

    return <div className={css.main}>
        <h4>Puerta {data.gateName}, {suma} ingresos</h4>
        { 
            data.accessDevices.map((item, index)=><Turnstile key={`ttl${index}`} data={item} />) 
        }
    </div>
}