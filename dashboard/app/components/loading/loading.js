"use client"
import css from "@/app/styles/loading.module.css"
import Cookies from "js-cookie";

import { store_container } from "@/app/stores/container"
import { store_token } from "@/app/stores/token"
import { store_auth } from "@/app/stores/auth" 
import { store_notification } from "@/app/stores/notification";

import { useEffect } from "react"

import { update_data } from "@/app/hooks/update_data";

import { store_events_list } from "@/app/stores/events_list";
import { store_events_current } from "@/app/stores/events_current";
import { store_events_stats } from "@/app/stores/events_stats";

export default function Loading () { 

    const { set_message } = store_notification()
    const { set_container } = store_container()
    const { authentication, set_authentication } = store_auth()
    const { set_token } = store_token()

    const update_events_list = async () => {
        const endpoint = "events"
        const { set_data } = store_events_list()
        const { result, error } = await update_data(endpoint)
        if (error) set_message("error en el componente ", endpoint)
        if (result) set_data(result)
        //console.log("result event list: ", result)
    }
    update_events_list()

    const update_events_current = async () => {
        const endpoint = "events/current"
        const { set_data } = store_events_current()
        const { result, error } = await update_data(endpoint)
        if (error) set_message("error en el componente ", endpoint)
        if (result) set_data(result)
        //console.log("result events current: ", result)
    }
    update_events_current()

    const update_events_stats = async () => {
        const endpoint = "events/stats"
        const { set_data } = store_events_stats()
        const { result, error } = await update_data(endpoint)
        //if (error) set_message("error en el componente ", endpoint)
        if (result) set_data(result)
    }
    update_events_stats()

    useEffect(()=>{
        if (authentication) {  
            set_container("dashboard")
        } else {
            
            const token_auth_cookies = Cookies.get("token_auth")
            const token_auth_localStorage = localStorage.getItem("token_auth")
            const token_auth_sessionStorage = sessionStorage.getItem("token_auth")
            
            if (token_auth_cookies) {

                set_token(token_auth_cookies)
                set_authentication(true)
                set_container("dashboard")

            } else if (token_auth_localStorage) {

                set_token(token_auth_localStorage)
                set_authentication(true)
                set_container("dashboard")

            } else if (token_auth_sessionStorage) {

                set_token(token_auth_sessionStorage)
                set_authentication(true)
                set_container("dashboard")
                
            } else {
                set_container("login")
            }   
        }
    },[])



    return <div className={css.main}>
        <h3>Cargando datos...</h3>
    </div>
}
/*
        <Update_events_list />

*/