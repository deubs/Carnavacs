export const get_gates_id = async ( id ) => {
    const res = await fetch(`${process.env.get_gates_id}${id}`, {
      method: "get"
    })
    const response =  await res.json()
    return response 
    }
    