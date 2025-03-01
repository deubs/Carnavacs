"use client"
import { useEffect } from "react"
import css from "@/app/test/test.module.css"
import { store_test } from "./store"

export default function Test () {
  const { state, set_state } = store_test()

  useEffect(()=>{
    setTimeout(()=>{
      set_state("Componente")
    }, 2000)
  }, [])
  
  if (!state) {
      return <div className={css.main}>
      <p>Retorno por defecto</p>
      </div>
    } else {
      return <p>{ state }</p>
    }
} 
