"use client"
import css from "@/app/styles/button.module.css"

export default function Button ({ text, callback }) {
    return <button  
    onClick={callback}
    className={css.main}>{text}</button>
}