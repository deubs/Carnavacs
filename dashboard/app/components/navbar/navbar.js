"use client"
import styles from "@/app/styles/navbar.module.css"

import { RxHamburgerMenu } from "react-icons/rx";
import { useState } from "react"
import { store_loop } from "@/app/stores/loop";
import Sidebar from "@/app/components/navbar/components/sidebar";

export default function Navbar () {
    const { loop_status, change_status } = store_loop()
    const [ visible, setVisible ] = useState(false)

    const toggle = () => {
        setVisible(!visible)
    }

    return <div className={styles.main}>
        <div className={styles.loop_status}>
            <span><p>LS</p><p className={`${loop_status ? styles.on : styles.off }`}>{loop_status ? "ON" : "OFF"}</p></span>
            <button onClick={()=>{change_status()}}>Change</button>
        </div>

        <RxHamburgerMenu
        onClick={toggle}
        className={styles.icon}
        />
        <Sidebar visible={visible} />
        </div>
}
