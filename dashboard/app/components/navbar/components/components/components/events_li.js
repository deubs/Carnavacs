"use client" 
import css from "@/app/styles/events_li.module.css"
import Button from "@/app/components/common/button"

import { store_event_id } from "@/app/stores/event_id"

export default function Event_li ({ data }) {
    const { set_event_id } = store_event_id()

    const onClickEvent = () => {
        console.log("id del evento: ", data.id)
        set_event_id(data.id)
        //set_container("loading")    
    }

    return <div className={css.main}>
        <Button text={data.nombre} callback={onClickEvent}/>
    </div>
}