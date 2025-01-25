"use client"
import css from "@/app/styles/loading.module.css"

import { useEffect, useState } from "react";

import { store_container } from "@/app/stores/container";

import { store_event_id } from "@/app/stores/event_id";
import { store_events_current } from "@/app/stores/events_current";
import { store_events_list } from "@/app/stores/events_list";
import { store_events_stats } from "@/app/stores/events_stats";

import { update_data_post } from "@/app/hooks/update_data";
import { update_data } from "@/app/hooks/update_data";

export default function Loading () {

    const { set_container } = store_container()

    const { set_events_current } = store_events_current()
    const { set_events_list } = store_events_list()
    const { set_events_stats } = store_events_stats()
    const { event_id } = store_event_id()

    useEffect(()=>{
        
        set_events_current("loading")
        set_events_list("loading")
        set_events_stats("loading")
        
        update_data("events", set_events_list, event_id)
        update_data("events/current", set_events_current, event_id)
        update_data("events/stats", set_events_stats, event_id)
        /*
        update_data_post("events", set_events_list)
        update_data_post("events/current", set_events_current)
        update_data_post("events/stats", set_events_stats)
        */
        set_container("dashboard")

    }, [event_id])

    return <div className={css.main}>
        <h3>Cargando datos...</h3>
    </div>
}
