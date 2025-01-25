"use client"
import Cookies from "js-cookie";

import { store_auth } from "@/app/stores/auth"  
import { store_container } from "@/app/stores/container"
import { useEffect } from "react";


export const Loader_authentication = () => {

    const { authentication } = store_auth()
    const { set_container } = store_container()

    useEffect(()=>{

        if (authentication) {

            set_container("loading")

        } else {
            
            const token_auth_cookies = Cookies.get("token_auth")
            const token_auth_localStorage = localStorage.getItem("token_auth")
            const token_auth_sessionStorage = sessionStorage.getItem("token_auth")
            
            if (token_auth_cookies) {
        
                set_token(token_auth_cookies)
                set_container("loading")
        
            } else if (token_auth_localStorage) {
        
                set_token(token_auth_localStorage)
                set_container("loading")
        
            } else if (token_auth_sessionStorage) {
        
                set_token(token_auth_sessionStorage)
                set_container("loading")
                
            } else {

                set_container("login")

            }   
        }
    })
    return <></>
}