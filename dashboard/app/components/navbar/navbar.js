"use client"
import { RxHamburgerMenu } from "react-icons/rx";
import { useState } from "react"
import css from "./css.module.css"
import { store_dashboard } from "@/app/stores/dashboard";

export default function Navbar () {
    const { set_dashboard } = store_dashboard()
    const [ visible, setVisible ] = useState(false)

    const toggle = () => {
        setVisible(!visible)
    }

    return <div className={css.main}>

        <RxHamburgerMenu
        onClick={toggle}
        className={css.btn}
        />

        <div className={`${css.sidebar} ${visible && css.visible }`}>
            <button onClick={()=>{set_dashboard("home")}}>Inicio</button>
            <button onClick={()=>{set_dashboard("sector_stats")}}>Estadísticas por sectores</button>
        </div>
        </div>
}
