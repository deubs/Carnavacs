"use client"
import { useEffect } from "react";

import { useTimer } from "use-timer";
import { store_loop } from "@/app/stores/loop";
import { store_dashboard } from "@/app/stores/store_dashboard";

import { store_event_id } from "@/app/stores/event_id";
import { store_events_current } from "@/app/stores/events_current";
import { store_events_list } from "@/app/stores/events_list";
import { store_events_stats } from "@/app/stores/events_stats";
import { store_events_sector_stats } from "@/app/stores/events_sector_stats";

import { store_API_URL } from "@/app/stores/API_URL";
import { store_enviroment } from "@/app/stores/enviroment";

import { update_data } from "@/app/components/utils/update_data";
import { update_data_post } from "@/app/components/utils/update_data";

export default function Updates () {

    const { set_events_current } = store_events_current()
    const { set_events_list } = store_events_list()
    const { set_events_stats } = store_events_stats()
    const { set_sector_stats } = store_events_sector_stats()

    const { enviroment } = store_enviroment()
    const { container, set_container } = store_dashboard()

    const { API_URL } = store_API_URL()
    const { event_id } = store_event_id() 

    const { loop_status, change_status, tick, tick_increment } = store_loop()

    const update_data = () => {
        if (loop_status) {
            tick_increment()
        }
    }

    const { start, restart } = useTimer({
        interval: 2000,
        onTimeUpdate: ()=>{update_data()},
        autostart: false
    })
    
    useEffect(()=>{
        start()
    }, [API_URL])
    
    useEffect(()=>{
        if (container != "dashboard") set_container("dashboard")

        if (enviroment == "PROD") {

            update_data(API_URL, "events/current", set_events_current, change_status, event_id)
            update_data(API_URL, "events", set_events_list, change_status, event_id)
            update_data(API_URL, "events/stats", set_events_stats, change_status, event_id)
            update_data(API_URL, "events/sectorStats", set_sector_stats, change_status, event_id)

        } else if (enviroment == "DEV") {

            update_data_post("events/current", set_events_current, change_status)
            update_data_post("events", set_events_list, change_status)
            update_data_post("events/stats", set_events_stats, change_status)
            update_data_post("events/sectorStats", set_sector_stats, change_status)

        } else {
            console.log("error obteniendo datos") 
        }
 
    }, [tick, event_id])
    
    return <></>
}