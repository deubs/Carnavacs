"use client"
import css from "./css.module.css"
import { store_message } from "@/app/stores/message"

export default function Message () {
    const { message, set_message } = store_message()
    const reset_notif = () => {
        set_message(undefined)
    }
    return <div className={`${css.main} ${ message && css.visible }`}>
        <div className={css.container}>
        <p>{message}</p>
        <button onClick={reset_notif}>Aceptar</button>
        </div>
    </div>
}