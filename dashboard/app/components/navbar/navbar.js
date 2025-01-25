"use client"
import { RxHamburgerMenu } from "react-icons/rx";
import { useState } from "react"
import css from "@/app/styles/navbar.module.css"

import Sidebar from "./sidebar";

export default function Navbar () {
    const [ visible, setVisible ] = useState(false)

    const toggle = () => {
        setVisible(!visible)
    }

    return <div className={css.main}>
        <RxHamburgerMenu
        onClick={toggle}
        className={css.icon}
        />
        <Sidebar visible={visible} />
        </div>
}
