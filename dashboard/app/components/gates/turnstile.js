"use client"
import css from "@/app/styles/turnstile.module.css"

export default function Turnstile ({ data }) {
    return <>
    {
        data && <div className={css.main}>
            <div className={css.title}>
                <p>TANGO</p>
                <p className={css.number}>{data.deviceName.slice(-2)}</p>
            </div>
            <div className={css.content}>
                <p>INGRESOS</p>
                <p className={css.number}>{data.peopleCount}</p>
            </div>
    </div>
    }
    </>
}