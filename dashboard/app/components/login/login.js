"use client"
import Cookies from "js-cookie"
import css from "./css.module.css"

import { fetch_login } from "@/app/utils/login"
import { store_container } from "@/app/stores/container"
import { store_notification } from "@/app/stores/notification"


export default function Login () {
  const { set_container } = store_container()
  const { set_message } = store_notification()

  const checkCredentials = async ( form ) => {
    const user = form.get("user")
    const password = form.get("password")
    const rta = await fetch_login(user, password)
    if (rta.login) {
      
      Cookies.set("token_auth", rta.token, { secure: true })
      localStorage.setItem("token_auth", rta.token)
      sessionStorage.setItem("token_auth", rta.token)
      
      set_container("loading")
    } else {
      set_message("ERROR: credenciales incorrectas")
    }
  }
  
  return <form action={checkCredentials} className={css.main}>
        <h3>Iniciar sesión</h3>
        <p>Usuario</p>
        <input type="text" name="user" ></input>
        <p>Contraseña</p>
        <input type="password" name="password"></input>
        <input type="submit" value="Conectar"/>
      </form>
}
