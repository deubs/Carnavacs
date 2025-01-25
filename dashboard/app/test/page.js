"use client"
import { useEffect } from "react"

export default function Test () {

    return <button onClick={()=>{
        console.log(process.env.NEXT_PUBLIC_API_URL)
    }}>test</button>
} 