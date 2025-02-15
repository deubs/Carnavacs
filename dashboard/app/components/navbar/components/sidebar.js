"use client"
import css from "@/app/styles/sidebar.module.css"
import Events_list from "@/app/components/navbar/components/components/events_list";
import Button from "@/app/components/common/button";

import { store_dashboard } from "@/app/stores/store_dashboard";

export default function Sidebar ({ visible }) {
    
    const { set_container } = store_dashboard()

    const scan_qr = () => set_container("qr_scan")
    const inicio = () => set_container("dashboard")

    return <div className={`${css.main} ${visible && css.visible }`}>
        <Button text={"Inicio"} callback={inicio} />
        <Button text={"Escanear QR"} callback={scan_qr} /> 
        <Events_list />
        </div>
}