"use client"
import css from "./css.module.css"

export default function Sector_stat ({ data }) {

    return <div className={css.main}>
        <div className={css.left}>
        <p>Sector</p>
        <p>{data.name.toUpperCase()}</p>
        </div>
        <div className={css.right}>
        <p>Ventas</p>
        <p>{data.total}</p>
        </div>
    </div>
}