import { useEffect } from "react";
import { store_API_URL } from "@/app/stores/API_URL";
import { store_enviroment } from "@/app/stores/enviroment";
import { store_notification } from "@/app/stores/notification";

export default function  Enviroment () {
    const { set_API_URL } = store_API_URL()
    const { set_enviroment } = store_enviroment()
    const { set_message } = store_notification()

    useEffect(()=>{

        let url = window.location.href;

        if (url.includes("api")) {
            set_API_URL(process.env.NEXT_PUBLIC_APIURL_API)
            set_enviroment("PROD")

        } else if (url.includes("boleteria")) {
            set_API_URL(process.env.NEXT_PUBLIC_APIURL_BOLETERIA)
            set_enviroment("PROD")

        } else if (url.includes("localhost")) {
            set_API_URL(process.env.NEXT_PUBLIC_APIURL_DEV)
            set_enviroment("DEV")

        } else {
            console.log("Error obteniendo URL ENVIROMENT")
        }
    }, [])
    return <></>
}

