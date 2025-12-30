import { useEffect } from "react";
import { store_API_URL } from "@/app/stores/API_URL";
import { store_enviroment } from "@/app/stores/enviroment";

export default function  Enviroment () {
    const { set_API_URL } = store_API_URL()
    const { set_enviroment } = store_enviroment()

    useEffect(()=>{
        let url = window.location.href;

        if (url.includes("api")) {

            set_API_URL(process.env.NEXT_PUBLIC_APIURL_API)
            set_enviroment("PROD")
            console.log("enviroment setted up: prod, url: ", process.env.NEXT_PUBLIC_APIURL_API)

        } else if (url.includes("boleteria")) {

            set_API_URL(process.env.NEXT_PUBLIC_APIURL_BOLETERIA)
            set_enviroment("PROD")
            console.log("enviroment setted up: prod, url: ",process.env.NEXT_PUBLIC_APIURL_BOLETERIA)

        } else if (url.includes("localhost") || url.includes(192)) {

            set_API_URL(process.env.NEXT_PUBLIC_APIURL_DEV)
            set_enviroment("DEV")
            console.log("enviroment setted up: dev, url: ",process.env.NEXT_PUBLIC_APIURL_DEV)

        } else {

            console.log("Error obteniendo URL ENVIROMENT")
        }
    }, [])
    return <></>
}