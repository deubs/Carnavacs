import { NextResponse } from "next/server";
import jwt from "jsonwebtoken"

export async function POST ( req ) {
    const { event, data } = await req.json()

    const generarToken = () => new Promise((resolve, reject)=>{
        const  user = {
            id: 1,
            usr: "factoneta"
        }
        const options = {
            expiresIn: "2m"
        }
        jwt.sign(user, "password123", options, (error, token)=>{
            if(error) reject("error generando jwt")
            resolve(token)
        })
    })
    
    const verificarToken = (token) => new Promise((resolve, reject)=>{
        jwt.verify(token, "password123", (error, decoded)=>{
            if(error) reject("error verificando jwt: "+error)
            resolve("token correcto")
        })
    })

    switch (event) {
        case 1: 
            try {
                const { user, password } = data
                if( user == "asd" && password == "123") {
                    const token = await generarToken()
                    return NextResponse.json({ login: true, token })
                } else {
                    return NextResponse.json({ login: false })
                }

            } catch (error) {
                return NextResponse.json({ error })
            }
        case 2: 
            try {
                return NextResponse.json({
                    ok: true,
                    tickets: {
                        vendidos: 50000,
                        ingresos: 25000,
                        adultos: 15000,
                        menores: 9500,
                        otros: 500
                    },
                    ingresosPorHora: {
                        "20:00": 25000,
                        "21:00": 20000,
                        "22:00": 16000,
                        "23:00": 13000,
                        "00:00": 9000,
                        "01:00": 2000,
                        "02:00": 1000,
                        "03:00": 100,
                        "04:00": 20
                    }
                })
            } catch (error) {
                return NextResponse.json({ error })
            }
        case 3:
            try {
                const { token } = data
                const r = await verificarToken(token)
                return NextResponse.json({ r: "token correcto" })
            } catch (error) {
                return NextResponse.json({ error })
            }

        default: return NextResponse.json({ error: "evento default "})
    }
}

export async function GET ( req ) {
    return NextResponse.json({ error: "no get" })
}