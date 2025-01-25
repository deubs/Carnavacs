const users = [
    {
        user: "comision",
        password: "carnaval"
    },
    {
        user: "jose",
        password: "yanito"
    }
]

export const checkCredentials = (data) => {
    const { user, password } = data

    for(let x of users){
        if(x.user === user && x.password === password) return ({ login: true })
    }

    return ({ login: false })
}