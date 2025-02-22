"use client"
import { store_loop } from "@/app/stores/loop";
import { store_API_URL } from "@/app/stores/API_URL";
import { useEffect } from "react";
import { useTimer } from "use-timer"; 

export default function Timer () {
    const { API_URL } = store_API_URL()
    const { loop_status, change_status, tick_increment } = store_loop()

    const { start, pause } = useTimer({
        interval: 2000,
        onTimeUpdate: tick_increment, 
        autostart: false
    })

    useEffect(()=>{
        if (loop_status) {
            start()
            console.log("timer activado")
        } else {
            pause()
            console.log("timer desactivado")
        }
    }, [loop_status])
    
    useEffect(()=>{
        if (API_URL != undefined) {
            change_status(true)
        }
    }, [API_URL])

    return <></>
} 