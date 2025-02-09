"use client"
import { useEffect } from "react";

import { useTimer } from "use-timer";
import { store_loop } from "@/app/stores/loop";
import { store_notification } from "@/app/stores/notification";
import { store_container } from "@/app/stores/container";

import { store_event_id } from "@/app/stores/event_id";
import { store_events_current } from "@/app/stores/events_current";
import { store_events_list } from "@/app/stores/events_list";
import { store_events_stats } from "@/app/stores/events_stats";
import { store_events_sector_stats } from "@/app/stores/events_sector_stats";

import { store_API_URL } from "@/app/stores/API_URL";
import { store_enviroment } from "@/app/stores/enviroment";

import { update_data } from "@/app/querys/update_data";
import { update_data_post } from "@/app/querys/update_data";

export default function Updates () {

    const { set_message } = store_notification()
    const { set_events_current } = store_events_current()
    const { set_events_list } = store_events_list()
    const { set_events_stats } = store_events_stats()
    const { set_sector_stats } = store_events_sector_stats()

    const { enviroment } = store_enviroment()
    const { set_container } = store_container()

    const { API_URL } = store_API_URL()
    const { event_id } = store_event_id()

    const { loop_status, set_loop_status, tick, tick_increment } = store_loop()

    const { start, restart } = useTimer({
        interval: 2000,
        onTimeUpdate: tick_increment,
        autostart: false
    })
    /*
    useEffect(()=>{
            set_container("dashboard")
            update_data_post("events", set_events_list, set_loop_status)
            update_data_post("events/current", set_events_current, set_loop_status)
            update_data_post("events/stats", set_events_stats, set_loop_status)
            update_data_post("events/sectorStats", set_sector_stats, set_loop_status)
    }, [])
    */
    useEffect(()=>{
        set_loop_status(true)
        start()

    }, [API_URL])
    
    useEffect(()=>{
        set_container("dashboard")

        if (enviroment == "PROD") {

            update_data(API_URL, "events/current", set_events_current, set_loop_status, event_id)
            update_data(API_URL, "events", set_events_list, set_loop_status, event_id)
            update_data(API_URL, "events/stats", set_events_stats, set_loop_status, event_id)
            update_data(API_URL, "events/sectorStats", set_sector_stats, set_loop_status, event_id)

        } else if (enviroment == "DEV") {

            update_data_post("events/current", set_events_current, set_loop_status)
            update_data_post("events", set_events_list, set_loop_status)
            update_data_post("events/stats", set_events_stats, set_loop_status)

        } else {
            console.log("error obteniendo datos")
        }
 
    }, [tick])
    
    return <></>
}