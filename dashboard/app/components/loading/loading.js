"use client"
import css from "@/app/styles/loading.module.css"
import { useEffect } from "react";

import { store_container } from "@/app/stores/container";

import { store_event_id } from "@/app/stores/event_id";
import { store_events_current } from "@/app/stores/events_current";
import { store_events_list } from "@/app/stores/events_list";
import { store_events_stats } from "@/app/stores/events_stats";
import { store_loop } from "@/app/stores/loop";

import { update_data_post } from "@/app/hooks/update_data";
import { update_data } from "@/app/hooks/update_data";

import { get_type_url } from "@/app/components/common/get_type_url";
import { store_API_URL } from "@/app/stores/API_URL";

import { loop } from "../charts/loop";

export default function Loading () {

    const { set_container } = store_container()
    const { set_events_current } = store_events_current()
    const { set_events_list } = store_events_list()
    const { set_events_stats } = store_events_stats()
    const { event_id } = store_event_id()
    const { API_URL, set_API_URL } = store_API_URL()
    //const { loop_status, set_loop_status, count, count_increase } = store_loop()

    useEffect(()=>{
        
        const typeurl = get_type_url(window.location.href, set_API_URL)
        if (typeurl == "api") {
            set_API_URL(process.env.NEXT_PUBLIC_APIURL_API)
        } else {
            set_API_URL(process.env.NEXT_PUBLIC_APIURL_BOLETERIA)
        }

    }, [])

    /*
    useEffect(()=>{
        if (!loop_status) {
            set_loop_status(true)
            loop(count_increase)
        }
    }, [API_URL])
    */

    useEffect(()=>{

        if (API_URL != undefined) {

        set_events_current("loading")
        set_events_list("loading")
        set_events_stats("loading")
        
        update_data(API_URL, "events", set_events_list, event_id)
        update_data(API_URL, "events/current", set_events_current, event_id)
        update_data(API_URL, "events/stats", set_events_stats, event_id)

        /*
        update_data_post("events", set_events_list)
        update_data_post("events/current", set_events_current)
        update_data_post("events/stats", set_events_stats)
        */
        set_container("dashboard")
        }
        
    }, [API_URL])

    return <div className={css.main}>
        <h3>Cargando datos...</h3>
    </div>
}
