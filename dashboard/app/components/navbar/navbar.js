"use client"
import { RxHamburgerMenu } from "react-icons/rx";
import { useState } from "react"
import css from "./css.module.css"

export default function Navbar () {
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
            <button>test</button>
            <button>test</button>
            <button>test</button>
            <button>test</button>
        </div>
        </div>
}

/*
            <button onClick={()=>{setNight(1)}}>Noche 1</button>
            <button onClick={()=>{setNight(2)}}>Noche 2</button>
            <button onClick={()=>{setNight(3)}}>Noche 3</button>
            <button onClick={()=>{setNight(4)}}>Noche 4</button>
            <button onClick={()=>{setNight(5)}}>Noche 5</button>
            <button onClick={()=>{setNight(6)}}>Noche 6</button>
            <button onClick={()=>{setNight(7)}}>Noche 7</button>
            <button onClick={()=>{setNight(8)}}>Noche 8</button>
            <button onClick={()=>{setNight(9)}}>Noche 9</button>
            <button onClick={()=>{setNight(10)}}>Noche 10</button>
*/