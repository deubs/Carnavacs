"use client"
import css from "@/app/styles/qrcode_information.module.css"
import { store_ticket_validate } from "@/app/stores/ticket_validate";

export const QRCODE_information = () => {
    const { m1, m2, info } = store_ticket_validate() 

    return <div className={css.main}>
        <p>Resultado:</p>
        <p>{ m1 }</p>
        <p>{ m2 }</p>
        <p>{ info }</p>
    </div>
}
