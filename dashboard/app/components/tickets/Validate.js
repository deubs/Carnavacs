"use client"
import css from "./css.module.css"
import { store_ticket_validate } from "@/app/stores/ticket_validate";

export default function Ticket_validate () {
    const { m1, m2 } = store_ticket_validate()
    return <div className={css.main}>
        <p>Resultado:</p>
        <p>{m1}</p>
        <p>{m2}</p>
    </div>
}