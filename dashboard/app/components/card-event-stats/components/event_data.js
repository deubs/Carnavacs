import styles from "@/app/styles/event_data.module.css"
import { store_events_current } from "@/app/stores/events_current"
import { store_event_id } from "@/app/stores/event_id"
import { data_parse } from "@/app/components/utils/data_parse"
import { store_events_list } from "@/app/stores/events_list"
import { useEffect } from "react"

export default function Event_data () {
    const { events_current, set_events_current } = store_events_current()
    const { event_id } = store_event_id()
    const { events_list } = store_events_list()

    useEffect(()=>{
        if (event_id != undefined && events_list != "loading") {
            const actually = events_list.filter(event => event.id == event_id)
            set_events_current(actually[0])
        }
    },[event_id])

    return <div className={styles.main}>
        {
            events_current && <p>{`${events_current.nombre}, ${data_parse(events_current.fecha)}`}</p>
        }
    </div>
}
