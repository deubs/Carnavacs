"use client"
import { useState } from "react"
import css from "./css.module.css"
import { storeNoche } from "@/app/state/state"

const Navbar = () => {
    const [ state, setState ] = useState(false)
    const { noche, setNoche } = storeNoche()
    const toggle = () => {
        setState(!state)
    }
    return <div className={css.main}>
        <button className={css.btn} onClick={toggle}>OP</button>
        <div className={`${css.sidebar} ${state && css.visible}`}>
            <h2>Opciones</h2>
            <button onClick={()=>{setNoche(1)}}>Noche 1</button>
            <button onClick={()=>{setNoche(2)}}>Noche 2</button>
            <button onClick={()=>{setNoche(3)}}>Noche 3</button>
            <button onClick={()=>{setNoche(4)}}>Noche 4</button>
            <button onClick={()=>{setNoche(5)}}>Noche 5</button>
            <button onClick={()=>{setNoche(6)}}>Noche 6</button>
            <button onClick={()=>{setNoche(7)}}>Noche 7</button>
            <button onClick={()=>{setNoche(8)}}>Noche 8</button>
            <button onClick={()=>{setNoche(9)}}>Noche 9</button>
            <button onClick={()=>{setNoche(10)}}>Noche 10</button>
            </div>
        </div>
}

export {
    Navbar
}