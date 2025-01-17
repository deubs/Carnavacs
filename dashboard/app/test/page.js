"use client"

export default function Test () {

    const get = async () => {
        const r = await fetch("http://api.carnavaldelpais.com.ar/events")
        const rr = await r.json()
        console.log(rr)

    }
    return <div>
        <button onClick={get}>test 1</button>
    </div>
}