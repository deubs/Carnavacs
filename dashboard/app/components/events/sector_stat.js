"use client"
import css from "@/app/styles/sector.module.css"

export const Sector_stat = ({ data }) => {
    return <div className={css.main}>
        <p>{data.name}</p>
        <p>Ventas: {data.total}</p>
        <p>Ingresos: {data.readed}</p>
    </div>
}