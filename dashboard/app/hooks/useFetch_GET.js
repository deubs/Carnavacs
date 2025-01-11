import { useEffect, useState } from "react";

export async function useFetch_GET ( url ) {

    const [ loading, set_loading ] = useState(undefined)
    const [ data, set_data ] = useState(undefined)
    const [ error, set_error ] = useState(undefined)

    useEffect(()=>{
        const get_data = async () => {
            try {
                set_loading(true)
                const response = await fetch(url)
                const response_json = await response.json()

                if (response_json.success) {
                    console.log(response_json.result)
                    set_data(response_json.result)
                } else {
                    throw new Error("no es success")
                }
            } catch (error) {
                set_error(error)
            } finally {
                set_loading(false)
            }
        }
        get_data()
    },[url])

    return {
        loading,
        data,
        error
    }
}