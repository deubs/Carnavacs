"use client"
import { update_data_post } from "../hooks/update_data_post"

export default function Test () {

    const get = async ( url ) => {
        const { error, data } = await update_data_post(url)
        console.log(error, data)

    }
    return <div>
        <button onClick={()=>{get("events")}}>test 1</button>
        <button onClick={()=>{get("events/current")}}>test 2</button>
    </div>
}