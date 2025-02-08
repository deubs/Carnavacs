"use client" 
import css from "@/app/styles/events_li.module.css"
import Button from "../common/Button"

import { store_event_id } from "@/app/stores/event_id"
import { store_container } from "@/app/stores/container"

export default function Event_li ({ data }) {
    const { set_event_id } = store_event_id()
    const { set_container } = store_container()

    const onClickEvent = () => {
        console.log("id del evento: ", data.id)
        set_event_id(data.id)
        //set_container("loading")    
    }

    return <div className={css.main}>
        <Button texto={data.nombre} onClick={onClickEvent}/>
    </div>
}