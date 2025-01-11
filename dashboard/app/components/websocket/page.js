"use client"
import io from 'socket.io-client';
import css from "./css.module.css"

import { storeTurnstiles } from '../state/state';
import { useEffect, useState } from 'react';

import { event_entry_failed, event_entry_passed, event_status, event_error } from './test_t_events';

export default function Websocket () {
    // import state handler
    const { handleTurnstile, add_error_log, error_log } = storeTurnstiles()
    // local state socket
    const [ newSocket, setSocket ] = useState()

    const [ number, setNumber ] = useState("no selected")

    useEffect(()=>{
        if (!newSocket) {
        const socket = io("ws://localhost:3000")

        // EVENT HANDLER

        socket.on("connect", () => {
            console.log("conectado al servidor")
            setSocket(socket)
        })
        socket.on("disconnect", () => {
            console.log("desconectado del servidor")
            return () => {
                socket.disconnect()
            }
        })
        socket.on("broadcast", (data) => {
            console.log("nuevo mensaje del server: ", data)
        })
        socket.on("turnstile_event", (data) => { 

            if (data.event == "status") {
                handleTurnstile(data.turnstile_id, data.event, data.status)
            } 
            if (data.event == "entry") {
                if (data.status == "success") {
                    handleTurnstile(data.turnstile_id, data.event, data.status)
                }
                if (data.status == "failure") {
                    handleTurnstile(data.turnstile_id, data.event, data.status)
                }
            }
            if (data.event == "error") {
                add_error_log(data)
            } 

        })
        return () => { socket.disconnect() }
        }
    },[])

    const ccheck = () => {
        newSocket.emit("checkSockets")
    }
    const desconectar = () => {
        newSocket.disconnect()
    }
    const new_turnstile_event = (data) => {
        newSocket.emit("turnstile_event", data) 
    }
    
    const event_turnstile_status_on = () => {
        const ticket_event = event_status(`turnstile_${number}`, 1)
        new_turnstile_event(ticket_event)
    }

    const event_turnstile_status_off = () => {
        const ticket_event = event_status(`turnstile_${number}`, 3)
        new_turnstile_event(ticket_event)

    }
    const event_turnstile_ticket_passed = () => {
        const ticket_event = event_entry_passed(`turnstile_${number}`)
        new_turnstile_event(ticket_event)

    }
    const event_turnstile_ticket_failure = () => {
        const ticket_event = event_entry_failed(`turnstile_${number}`)
        new_turnstile_event(ticket_event)

    }
    const event_turnstile_error = () => {
        const ticket_event = event_error(`turnstile_${number}`)
        new_turnstile_event(ticket_event)

    }
    const event_get_error_log = () => {
        console.log(error_log)
    }

    return <div className={css.main}> 
        <h3>websockets events</h3>
        <fieldset className={css.select}>
            <p>turnstile selected: { number } </p>
            <input placeholder='turnstile' onChange={(e)=>{setNumber(e.target.value)}}></input>
        </fieldset>
        <fieldset>
            <button onClick={event_get_error_log}>get errors log</button>
            <button onClick={event_turnstile_status_on}>turstile event status on</button>
            <button onClick={event_turnstile_status_off}>turstile event status off</button>
            <button onClick={event_turnstile_ticket_passed}>turstile event ticket passed</button>
            <button onClick={event_turnstile_ticket_failure}>turstile event ticket failure</button>
            <button onClick={event_turnstile_error}>turstile event error</button>
        </fieldset>
    </div>
}



/* 
const simularTickets = () => {

        const simular_ticket = (puerta, value) => {
            // handleTurnstile()  
        }
        const lowChance = () => {
            return Math.random() < 0.99
        }
        const st = async () => {
            for (let i = 1; i < 25; i++) {
                for (let t = 0; t < nroSimular; t++) {
                    const r = lowChance()
                    simular_ticket(`p${i}`, r)
                }
            }
        }
        st()
    }

    const activarPuertas = () => {
        for (let i = 1; i < 25; i++) {
            new_turnstile_event(`p${i}`, "status", 1)
        }
    }
*/