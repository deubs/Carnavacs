'use server' 
export const load_enviroment = async () => {
    const LOCAL_API_URL = process.env.LOCAL_API_URL
    const API_URL = process.env.API_URL
    return ({ LOCAL_API_URL, API_URL })
}