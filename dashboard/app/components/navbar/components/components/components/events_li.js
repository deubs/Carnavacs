"use client" 
import css from "@/app/styles/events_li.module.css"
import Button from "@/app/components/common/button"

import { store_event_id } from "@/app/stores/event_id"
import { store_dashboard } from "@/app/stores/store_dashboard"

export default function Event_li ({ data, callback }) {
    const { set_event_id } = store_event_id()
    const { set_container } = store_dashboard()

    const onClickEvent = () => {
        callback()
        set_event_id(data.id)
        set_container("dashboard")
    }

    return <div className={css.main}>
        <Button text={data.nombre} callback={onClickEvent}/>
    </div>
}
