"use client"
import styles from "@/app/styles/all_nights.module.css"
import Card from "@/app/components/common/card"

import { Error } from "@/app/components/common/error"
import { Loading } from "@/app/components/common/loading"

import { store_events_current } from "@/app/stores/events_current"
import { store_events_list } from "@/app/stores/events_list"
import { store_API_URL } from "@/app/stores/API_URL"
import { store_all_stats } from "@/app/stores/stats_all_nights"
import { useEffect, useState } from "react"

import { update_data_nights } from "@/app/components/utils/update_data"

import Chart from "@/app/components/card-all-nights/components/Line_chart"

export default function All_nights () {

    const { API_URL } = store_API_URL()
    const { events_current } = store_events_current()
    const { events_list } = store_events_list()
    const { nights, set_nights, data, set_data, state, set_state} = store_all_stats()

    useEffect(()=>{ 
        if (events_list != "loading" && events_current != "loading") {
            if (state != "ready") {
            const actually = events_current.id
            const targets = []
            
            for (let event of events_list) {
                if (event.id <= actually) {
                    let target = {
                        nombre: event.nombre.split(" ").slice(0,2).reverse().toString().replace(","," "),
                        id: event.id
                    }
                    targets.push(target)
                }
            }
            set_nights(targets)
        }
    }
    }, [events_list, events_current])

    useEffect(()=>{

        for (let night of nights) {
            const get_quantity = async () => {
                const quantity = await update_data_nights(API_URL, night.id)
                night.quantity = quantity
                set_data(night)
                set_state("ready")
            }
            get_quantity()
        }

    },[nights])

    return <Card>
        <h3>ESTADÍSTICAS DE TEMPORADA</h3>
        {
            state == "loading" ? <Loading /> : 
            state == "error" ? <Error /> :
            <div className={styles.main}>
                <p>Tickets totales: {data.reduce((accumulator, current)=> accumulator + current.quantity, 0)}</p>
                <Chart/>
            </div>
        }
    </Card>
}