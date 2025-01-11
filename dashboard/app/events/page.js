"use client"

export default function Events () {

    const test = async ( evento ) => {
        const r = await fetch(`http://api.carnavaldelpais.com.ar/Events/Stats`)
        const rr = await r.json()
        console.log(rr)
    }
    return <div>
        <button onClick={()=>{test("events")}}>sadasdcheck</button>
        <button onClick={()=>{test("events_current")}}>check</button>
        <button onClick={()=>{test("events_stats")}}>check</button>
        <button onClick={()=>{test("gates")}}>check</button>
        <button onClick={()=>{test("gates_id")}}>check</button>

    </div>
}




    /*
    if (response.success) {
                for (let x of response.result) {
                    console.log(new Date(x.fecha).toLocaleDateString("es-ES", {
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit"
                    }))
                }
            }
    */