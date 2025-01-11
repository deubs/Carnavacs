"use client"
import css from "./css.module.css"

import Cookies from "js-cookie";

import { store_container } from "@/app/stores/container"
import { store_token } from "@/app/stores/token"
import { store_auth } from "@/app/stores/auth" 
import { useEffect } from "react"

export default function Loading () {
    const { set_container } = store_container()
    const { authentication, set_authentication } = store_auth()
    const { set_token } = store_token()

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