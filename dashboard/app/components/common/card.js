"use client"
import css from "@/app/styles/card.module.css"

export default function Card ({ children }) {
return <div className={css.main}>{ children }</div>
}