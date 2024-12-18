"use client"
import css from "./css.module.css"
import { storePuertas } from "@/app/state/state"
import { Puerta } from "../puerta/puerta"

const Puertas = () => {
    const { p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
            p11, p12, p13, p14, p15, p16, p17, p18, p19, p20,
            p21, p22, p23, p24 } = storePuertas()

    return <div className={css.main}>
        <h3>Puertas, Acceso Norte</h3>
        <h4>Ayacucho:</h4>
        <div className={css.contenedorPuertas}>
            <Puerta data={p1}/>
            <Puerta data={p2}/>
            <Puerta data={p3}/>
            <Puerta data={p4}/>
            <Puerta data={p5}/>
            <Puerta data={p6}/>
            <Puerta data={p7}/>
            <Puerta data={p8}/>

        </div>
        <h3>Acceso Sur</h3>
        <h4>Ayacucho:</h4>
        <div className={css.contenedorPuertas}>
            <Puerta data={p9}/>
            <Puerta data={p10}/>
            <Puerta data={p11}/>
            <Puerta data={p12}/>
            <Puerta data={p13}/>
            <Puerta data={p14}/>
            <Puerta data={p15}/>
            <Puerta data={p16}/>
        </div>
        <h4>Maipú:</h4>
        <div className={css.contenedorPuertas}>
            <Puerta data={p17}/>
            <Puerta data={p18}/>
            <Puerta data={p19}/>
            <Puerta data={p20}/>
            <Puerta data={p21}/>
            <Puerta data={p22}/>
            <Puerta data={p23}/>
            <Puerta data={p24}/>
        </div>
    </div>
} 

export {
    Puertas
}