"use client"
import css from "./css.module.css"

import { useEffect } from "react"
import { store_message } from "@/app/stores/message"
import { update_data } from "@/app/hooks/update_data"

import { sector_stats } from "@/app/stores/sector_stats"

import Sector_stat from "../sector_stat/sector_stat"

export default function Sector_stats () {

    const { data, set_data } = sector_stats()
    const { set_message } = store_message()
    
    useEffect(()=>{
        const get = async () => {
            const { error, data } = await update_data("http://api.carnavaldelpais.com.ar/events/sectorStats")
            if (error)  set_message(`Error: compruebe el estado de la conexion a la red`)
            if (data)   set_data(data)
            console.log("data de sectores: ",data)
        }
        get()
    },[])

    return <div className={css.main}>
        {
        data &&
        data.map((item, index) => <Sector_stat data={item} key={index + 800} />)
        }
    </div>
}