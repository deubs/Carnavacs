import { useEffect, useState } from "react";

export async function useFetch_POST ( url, json ) {
    const [ is_loading, set_loading ] = useState(undefined)
    const [ is_data_fetched, set_data_fetched ] = useState(undefined)
    const [ is_error, set_error ] = useState(undefined)

    const getData = async () => {
        try {
            set_loading(true)
            const response = await fetch(url, {
                method: "post",
                headers: new Headers({"content-type":"application/json"}),
                body: JSON.stringify(json)
            })
            const response_json = await response.json()
            if (response_json.success) {
                set_loading(false)
                set_data_fetched(response)
            } else {
                throw new Error(`Error fetcheando data en url: ${url}`)
            }
        } catch (error) {
            set_error(error)
        }
    }
    useEffect(()=>{
        getData()
    },[url])

    return {
        is_loading,
        is_data_fetched,
        is_error
    }
}