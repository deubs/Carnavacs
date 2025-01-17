"use client"
import css from "@/app/styles/events_li.module.css"
import Button from "../common/Button"
// definir si esta habilitado o no con un iconito o algo en la prop "habilitado"
export default function Event_li ({ data }) {
    const onClickEvent = () => {
        console.log("evento click, id: ", data.id)
    }
    // definir evento onclick
    return <div className={css.main}>
        <Button texto={data.nombre} onClick={onClickEvent}/>
    </div>
}