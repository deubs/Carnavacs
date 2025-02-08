"use client"
import css from "./page.module.css"

import { store_container } from "./stores/container"

import Login from "./components/login/login"
import Dashboard from "./dashboard/dashboard"
import Message from "./components/notification/Notification"
import Enviroment from "./components/enviroment/Enviroment"
import Loading from "./components/loading/loading"
import Updates from "./components/updates/updates"

export default function Home () {
  const { container } = store_container()

  return <div className={css.main}>
    <Message />
    <Enviroment />
    <Updates />
    
    {
      container == "loading" ? <Loading /> :
      container == "login" ? <Login /> :
      container == "dashboard" ? <Dashboard /> :
      container == "qr" ? <Qr_scanner /> :
      "Error en cliente"
    }
  </div>
}
