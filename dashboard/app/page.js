"use client"
import css from "./page.module.css"
import { login } from "./utils/login";
import { redirect } from "next/navigation"
import Cookies from "js-cookie";

export default function Home() {

  const checkCredentials = async ( form ) => {
    const user = form.get("user")
    const password = form.get("password")
    const rta = await login(user, password)
    if (rta.login) {
      Cookies.set("Auth", rta.token, { secure: true })
      redirect("/dashboard")
    } else {
      alert("Credenciales incorrectas")
    }
  }

  return (
    <div className={css.main}>
      <form action={checkCredentials}>
        <h3>Iniciar sesión</h3>
        <p>Usuario</p>
        <input type="text" name="user" ></input>
        <p>Contraseña</p>
        <input type="password" name="password"></input>
        <input type="submit" value="Conectar"/>
      </form>
    </div>
  );
}
