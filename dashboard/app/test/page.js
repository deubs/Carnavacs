"use client"
import { store_enviroment } from "../stores/enviroment"

export default function Test () {
    const { API_URL, LOCAL_API_URL } = store_enviroment()
    const check = () => {
        console.log(API_URL, LOCAL_API_URL )
    }
    return <button onClick={check}>check</button>
}