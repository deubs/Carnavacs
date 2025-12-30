"use client"
import styles from "@/app/styles/gate.module.css"
import Turnstile from "@/app/components/card-turnstiles/components/components/turnstile"

export default function Gate ({ data }) {

    const suma = data.accessDevices.reduce((acumulacion, item)=>acumulacion + item.peopleCount, 0)
    //console.log("componente gate recibe: ",data)
    
    return <div className={styles.main}>
        <p>Puerta {data.gateName}, {suma} ingresos</p>
        { 
            data.accessDevices.map((item, index)=><Turnstile key={`ttl${index}`} data={item} />) 
        }
    </div>
}
