"use client"
import css from "./page.module.css"

import { store_container } from "./stores/container"

import Login from "./components/login/login"
import Dashboard from "./dashboard/dashboard"
import Loading from "./components/loading/loading"
import Message from "./components/notification/Notification"

export default function Container_main () {

  const { container } = store_container()

  return <div className={css.main}>
    <Message />
    {
      container == "login" ? <Login /> : 
      container == "dashboard" ? <Dashboard /> : 
      container == "loading" ? <Loading /> : 
      "Error en cliente"
    }
  </div>
}