"use client"
import css from "./css.module.css"

const Puerta = ({ data }) => {
    
    return <div className={css.main}>
        <p className={css.tpuerta}>{data.id}</p>
         <p>Estado <span className={data.estado ? css.verde : css.rojo }>{ data.estado ? "Activa" : "Inactiva" }</span></p>
         <p>Ingresos correctos <span className={css.invert}>{data.tickets.correctos}</span></p>
         <p>Ingresos rechazados <span className={css.invert}>{data.tickets.rechazados}</span></p>
    </div>
} 

export { 
    Puerta
}