"use client"
import css from "@/app/styles/events_sector_stats_area.module.css"

export const Sector_stats_area = ({ data }) => {
    return <div className={css.main}>

    <p className={css.type}>{ data.type }</p>
    <p className={`${css.sector} ${ (data.type == "SILLAS" || "SILLAS VIP" || "PULLMAN") && css.sillas } ${ data.type == ("SECTOR VIP" || "TRIBUNA") && css.vip }`}>{ data.sector }</p>
    <p className={css.type}>INGRESOS</p>
    <p className={css.quantity}>{ data.quantity }</p>

</div>
}