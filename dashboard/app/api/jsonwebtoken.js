import jwt from "jsonwebtoken"

export const generate_token = (user) => new Promise((resolve, reject) => {
        const data = {
            tokenGeneration: new Date().toLocaleString(),
            user: user
        }
        const options = {
            expiresIn: "2m"
        }
        jwt.sign(data, process.env.JWT, options, (error, token)=>{
            console.log(error)
            if(error) {
                reject("error generando jwt")
            }
            resolve(token)
        })
    })
    
export const check_token = (token) => new Promise((resolve, reject)=>{
        jwt.verify(token, process.env.JWT, (error, decoded)=>{
            if(error) reject("error verificando jwt: "+error)
            resolve("token correcto")
        })
    })