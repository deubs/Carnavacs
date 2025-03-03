import styles from "@/app/styles/event_data.module.css"
import { store_events_current } from "@/app/stores/events_current"
import { data_parse } from "@/app/components/utils/data_parse"

export default function Event_data () {
    const { events_current } = store_events_current()

    return <div className={styles.main}>
        <p>{ events_current && `${events_current.nombre}, ${data_parse(events_current.fecha)}`}</p>
    </div>
}