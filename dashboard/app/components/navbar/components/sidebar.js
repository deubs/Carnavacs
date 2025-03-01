"use client"
import css from "@/app/styles/sidebar.module.css"
import styles from "@/app/styles/navbar.module.css"

import Events_list from "@/app/components/navbar/components/components/events_list";
import Button from "@/app/components/common/button";
import { store_loop } from "@/app/stores/loop";
import { store_dashboard } from "@/app/stores/store_dashboard";

export default function Sidebar ({ visible, toggleVisible }) {
    const { set_container } = store_dashboard()
    const { loop_status, change_status } = store_loop()

    const scan_qr = () => {
        toggleVisible()
        set_container("qr_scan")
    }
    const inicio = () => {
        toggleVisible()
        set_container("dashboard")
    }
    
    return <div className={`${css.main} ${visible && css.visible }`}>
        <Button text={"Inicio"} callback={inicio} />
        <Button text={"Escanear QR"} callback={scan_qr} />  
        <Events_list callback={toggleVisible} />
        <div className={styles.loop_status}>
            <span><p>Loop status</p><p className={`${loop_status ? styles.on : styles.off }`}>{loop_status ? "ON" : "OFF"}</p></span>
            <button onClick={()=>{change_status(!loop_status)}}>Change</button>
        </div> 
        </div>
}