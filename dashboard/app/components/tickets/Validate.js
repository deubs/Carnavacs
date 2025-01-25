"use client"
import css from "@/app/styles/ticket_validation.module.css"
import { store_ticket_validate } from "@/app/stores/ticket_validate";

export const Ticket_validation = () => {
    const { m1, m2 } = store_ticket_validate() 

    return <div className={css.main}>
        <p>Resultado:</p>
        <p>{m1}</p>
        <p>{m2}</p>
    </div>
}
