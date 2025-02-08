"use client"
import css from "@/app/styles/sidebar.module.css"
import Events_list from "../events/Events_list";
import Button from "../common/Button";

import { store_dashboard } from "@/app/stores/store_dashboard";

export default function Sidebar ({ visible }) {
    
    const { set_container } = store_dashboard()

    const scan_qr = () => set_container("qr_scan")
    const inicio = () => set_container("home")

    return <div className={`${css.main} ${visible && css.visible }`}>
        <Button texto={"Inicio"} onClick={inicio} />
        <Button texto={"Escanear QR"} onClick={scan_qr} />
        <Events_list />
        </div>
}