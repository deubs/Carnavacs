"use client"
import css from "./css.module.css"
import { useEffect, useState } from "react"

import { store_message } from "@/app/stores/message"
import { update_data } from "@/app/hooks/update_data"
import Access_point from "../access_point/access_point"


export default function Access_points () {

    const [ gates, set_gates ] = useState()
    const { set_message } = store_message()

    useEffect(()=>{
        const get = async () => {
            const { error, data } = await update_data("http://api.carnavaldelpais.com.ar/events/stats")
            if (error)  set_message(`Error: compruebe el estado de la conexion a la red`)
            if (data)   set_gates(data.gates)
        }
        get()
    },[])
    
    return <div className={css.main}>
        { 
        gates && 
        gates.map(
            (item, index) => <Access_point data={ item } key={index + 999} />)
        }
    </div>
}