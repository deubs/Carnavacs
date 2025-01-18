"use client"
import css from "@/app/styles/turnstile.module.css"

export default function Turnstile ({ data }) {
    return <>
    {
        data && <div className={css.main}>
        <p>Tango {data.deviceName.slice(-2)}</p>
        <p>Ingresos: {data.peopleCount}</p>
    </div>
    }
    </>
}