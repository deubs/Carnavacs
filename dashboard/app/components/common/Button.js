"use client"
import css from "@/app/styles/button.module.css"

export default function Button ({ texto, onClick }) {
    return <button  
    onClick={onClick}
    className={css.main}>{texto}</button>
}