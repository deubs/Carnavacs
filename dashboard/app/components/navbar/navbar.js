"use client"
import styles from "@/app/styles/navbar.module.css" 
import Sidebar from "@/app/components/navbar/components/sidebar";
import { RxHamburgerMenu } from "react-icons/rx";
import { useState } from "react"

export default function Navbar () {
    const [ visible, setVisible ] = useState(false)

    const toggle = () => { 
        setVisible(!visible)
    }

    return <div className={styles.main}>
        <RxHamburgerMenu 
        onClick={toggle}
        className={styles.icon}
        />
        <Sidebar visible={visible} toggleVisible={toggle}/>
        </div>
}

/*
<img
        src="/logo.png"
        />
*/