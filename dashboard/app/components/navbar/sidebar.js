"use client"
import css from "@/app/styles/sidebar.module.css"
import { store_dashboard } from "@/app/stores/dashboard";
import Events_list from "../events/Events_list";


export default function Sidebar ({ visible }) {
    const { set_dashboard } = store_dashboard()

    return <div className={`${css.main} ${visible && css.visible }`}>
        <Events_list />
        </div>
}

/* 
<button onClick={()=>{set_dashboard("home")}}>Inicio</button>
            <button onClick={()=>{set_dashboard("sector_stats")}}>Estadísticas por sectores</button>
*/