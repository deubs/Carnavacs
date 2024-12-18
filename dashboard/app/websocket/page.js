"use client"
import io from 'socket.io-client';
import css from "./css.module.css"

import { storePuertas } from '../state/state';
import { useEffect, useState } from 'react';

export default function Websocket () {
    // prod
    const { handlePuerta } = storePuertas()
    const [ newSocket, setSocket ] = useState()
    // test
    const [ puerta, setPuerta ] = useState()
    const [ nroSimular, setNroSimular ] = useState()

    useEffect(()=>{
        if (!newSocket) {
            
        const socket = io("ws://localhost:3000")

        // eventos ws

        socket.on("connect", ()=>{
            console.log("conectado al servidor")

            setSocket(socket)
        })

        socket.on("disconnect", ()=>{
            console.log("desconectado del servidor")
            return () => {
                socket.disconnect()
            }
        })

        socket.on("puerta", (data) => {
            console.log("recibiendo evento por websocket: "+ JSON.stringify(data))
            const { puerta, evento, valor } = data
            handlePuerta(puerta, evento, valor )
        })

        socket.on("broadcast", (data) => {
            console.log("nuevo mensaje del server: ", data)
        })

        return () => {
            socket.disconnect()
        }
        }
    },[])

    const ccheck = () => {
        newSocket.emit("checkSockets")
    }
    const desconectar = () => {
        newSocket.disconnect()
    }
    const togglePuerta = (puerta, evento, valor) => {
        newSocket.emit("puerta", { puerta, evento, valor }) 
    }
    const activarPuertas = () => {
        for (let i = 1; i < 25; i++) {
            togglePuerta(`p${i}`, "estado", true)
        }
    }
    const simularTickets = () => {

        const ticket = (puerta, value) => {
            togglePuerta(puerta, "ticket", value ? "correcto" : "rechazado")
        }
        const lowChance = () => {
            return Math.random() < 0.99
        }
        const st = async () => {
            for (let i = 1; i < 25; i++) {
                for (let t = 0; t < nroSimular; t++) {
                    const r = lowChance()
                    ticket(`p${i}`, r)
                }
            }
        }
        st()
    }

    return <div className={css.main}>
        <span>
        <button onClick={activarPuertas}>activar puertas</button>
        <button onClick={desconectar}>desconectar ws</button>
        <button onClick={ccheck}>checkear sockets</button>
        </span>
        <div className={css.togglePuertas}>
            <input placeholder='puerta' onChange={(e)=>setPuerta(e.target.value)} />
            <span>
                <button onClick={()=>{togglePuerta(puerta, "estado", true)}}>Prender</button>
                <button onClick={()=>{togglePuerta(puerta, "estado", false)}}>Apagar</button>
            </span>
            <span>
                <button onClick={()=>{togglePuerta(puerta, "ticket", "correcto")}}>ticket correcto</button>
                <button onClick={()=>{togglePuerta(puerta, "ticket", "rechazado")}}>ticket rechazado</button>
            </span>
        </div>
        <div className={css.togglePuertas}>
            <input type='number' onChange={(e)=>{setNroSimular(e.target.value)}}/>
            <button onClick={simularTickets}>simular</button>
        </div>
    </div>
}