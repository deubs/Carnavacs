"use client"
import styles from "@/app/styles/all_nights.module.css"
import { useEffect, useState } from "react" 

import { Error } from "@/app/components/common/Error"
import { Loading } from "@/app/components/common/Loading"

import { store_events_current } from "@/app/stores/events_current"
import { store_events_list } from "@/app/stores/events_list"
import { store_API_URL } from "@/app/stores/API_URL"
import { store_stats_all_nights } from "@/app/stores/stats_all_nights"

import { get_total_tickets } from "@/app/components/utils/update_data"
import { get_nights } from "@/app/components/utils/get_nights"

import Card from "@/app/components/common/Card"
import Chart from "@/app/components/card-all-nights/components/line_chart"

export default function All_nights () {

    const { add_night, state_data, set_state_data, total_tickets, add_total_tickets, set_actually_night } = store_stats_all_nights()  
    const { API_URL } = store_API_URL() 
    const { events_current } = store_events_current()
    const { events_list } = store_events_list() 

    const [ previous_nights_without_quantities, set_previous_nights_without_quantities ] = useState([])

    useEffect(()=>{
        if (state_data == 0) {
            if (events_list != "loading" && events_current != "loading") {
                const nights_without_quantities = get_nights(events_current.id, events_list)
                set_previous_nights_without_quantities(nights_without_quantities) 
                set_state_data(1)
            }
        }
    },[events_list])
 
    useEffect(()=>{
        if (state_data == 1) {
            const get_quantities = async () => {
                for (const night of previous_nights_without_quantities) {
                    const { error, quantity } = await get_total_tickets(API_URL, night.id)
                    if (!error) {
                        const fullnight = {
                            name: night.name,
                            id: night.id,
                            quantity
                        }
                        if (previous_nights_without_quantities.indexOf(night) < previous_nights_without_quantities.length - 1) {
                            add_total_tickets(total_tickets + quantity)
                            add_night(fullnight)
                        } else {
                            set_actually_night(fullnight)                           
                        }
                    } else {
                        set_state_data(2)
                        break;
                    } 
                }
            }
            get_quantities()
            set_state_data(3)
        }
    },[previous_nights_without_quantities])

    return <Card>
        <h3>ESTADÍSTICAS DE TEMPORADA</h3>
        {
            state_data == 1 ? <Loading /> : 
            state_data == 2 ? <Error /> :
            <div className={styles.main}>
                <p>Tickets totales: { total_tickets }</p>
                <Chart/>
            </div>
        }
    </Card>
}
