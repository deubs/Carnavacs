"use client"
import css from "@/app/styles/events_list.module.css"
import { store_events_list } from "@/app/stores/events_list"

import Event_li from "./events_li"

export default function Events_list () {
    const { loaded, data } = store_events_list()

    return <div className={css.main}>
        {
            loaded && data.map( (item, index) => <Event_li key={`e_li${index}`} data={item} />)
        }       
    </div>
}