export const get_all_gates = async () => {
    const res = await fetch(`${process.env.get_all_gates}`, {
      method: "get"
    })
    const response =  await res.json()
    return response 
    }
    