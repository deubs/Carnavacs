"use client"
import { useEffect } from "react"
import { store_loop } from "@/app/stores/loop"

export default function Test () {
    const { loop_status, set_loop_status, count, count_increase } = store_loop()

    return <div>
        <p>contador: {count}</p>
        <p>estado: {loop_status}</p>
        <button onClick={()=>{count_increase()}}>incrementar</button>
        <button onClick={()=>{console.log(loop_status)}}>console log estado</button>
        <button onClick={()=>{set_loop_status(!loop_status)}}>change ls</button>
    </div>
} 