import styles from "@/app/styles/tickets_quantity.module.css"
import { store_events_stats } from "@/app/stores/events_stats"

export default function Tickets_quantity () {
    const{ events_stats } = store_events_stats()
    
    return <div className={styles.main}>
        <div className={styles.box}>
            <p>Ventas totales: { events_stats.totalTickets }</p>
        </div>
        <div className={styles.box}>
            <p>Ingresos: { events_stats.usedTickets }</p>
        </div>
        <div className={styles.box}>
            <p>Restantes: { events_stats.remainingTickets }</p>
        </div>
    </div>
}