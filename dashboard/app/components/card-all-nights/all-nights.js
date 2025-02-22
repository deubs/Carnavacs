"use client"
import styles from "@/app/styles/all_nights.module.css"
import { useEffect, useState } from "react" 
import Card from "@/app/components/common/Card"

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

import { store_events_current } from "@/app/stores/events_current"
import { store_events_list } from "@/app/stores/events_list"
import { store_API_URL } from "@/app/stores/API_URL"
import { store_stats_all_nights } from "@/app/stores/stats_all_nights"

import { get_total_tickets } from "@/app/components/utils/update_data"
import { get_nights } from "@/app/components/utils/get_nights"

import Chart from "@/app/components/card-all-nights/components/line_chart"

export default function All_nights () {

    const { previous_nights, add_night } = store_stats_all_nights() 
    const { API_URL } = store_API_URL()
    const { events_current } = store_events_current()
    const { events_list } = store_events_list()

    const [ previous_nights_without_quantities, set_previous_nights_without_quantities ] = useState([])
    const [ state_data, set_state_data ] = useState(0) 
    
    // agregar ese store al ultimo item del grafico
    // permitir que se actualize el ultimo item del grafico y lo anterior se mantenga
    // actualmente actualiza fulldata, falta configurar el grafico
    
    useEffect(()=>{
        if (state_data == 0) {
            if (events_list != "loading" && events_current != "loading") {
                const nights_without_quantities = get_nights(events_current.id, events_list)
                console.log("nights without quantities ",nights_without_quantities)
                set_previous_nights_without_quantities(nights_without_quantities)
                set_state_data(1)
                console.log("state data en 1")
            }
        }
    },[events_list])
 
    useEffect(()=>{
        if (state_data == 1) {
            const get_quantities = async () => { 
                for (const night of previous_nights_without_quantities) {
                    const quantity = await get_total_tickets(API_URL, night.id) 
                    const fullnight = {  
                        name: night.name,
                        id: night.id,
                        quantity
                    }
                    add_night(fullnight)
                }
            }
            get_quantities()
            set_state_data(2)
        }
    },[previous_nights_without_quantities])

    return <Card>
        <h3>ESTADÍSTICAS DE TEMPORADA</h3>
        {
            state_data != 2 ? <Loading /> : 
            //state_data == "error" ? <Error /> :
            <div className={styles.main}>
                <p>Tickets totales: </p>
                <Chart/>
            </div>
        }
    </Card>
}
