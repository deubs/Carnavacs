"use client"
import css from "@/app/styles/sidebar.module.css"
import { store_dashboard } from "@/app/stores/dashboard";
import Events_list from "../events/Events_list";
import Button from "../common/Button";

export default function Sidebar ({ visible }) {
    
    const { set_dashboard } = store_dashboard()
    const scan_qr = () => set_dashboard("qr_scan")
    const inicio = () => set_dashboard("home")

    return <div className={`${css.main} ${visible && css.visible }`}>
        <Button texto={"Inicio"} onClick={inicio} />
        <Button texto={"Escanear QR"} onClick={scan_qr} />
        <Events_list />
        </div>
}