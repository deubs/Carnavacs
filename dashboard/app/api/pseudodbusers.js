const users = [
    {
        user: "asd",
        password: "123"
    },
    {
        user: "pepe",
        password: "montana"
    }
]

export const checkCredentials = (data) => {
    const { user, password } = data

    for(let x of users){
        if(x.user === user && x.password === password) return ({ login: true })
    }

    return ({ login: false })
}