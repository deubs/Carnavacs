"use client"
import css from "./css.module.css"
import Navbar from "../navbar/navbar"
import Event_stats from "./events_stats/events_stats"
import Event_current from "./event_current/event_current"

import Access_points from "./gates/access_points"

export default function Dashboard () {
    return <div className={css.main}>
      <Navbar />  
      <Event_stats />
      <Access_points />
      </div>
}
 
/*
        
      <Event_current />
      
      

{
  "success": true,
  "message": null,
  "result": [
    {
      "id": 86,
      "nroSerie": "192.168.40.131",
      "accesoSectorFk": 1,
      "puertaIngresoId": 2
    },
    {
      "id": 106,
      "nroSerie": "192.168.40.16",
      "accesoSectorFk": 1,
      "puertaIngresoId": 2
    },
    {
      "id": 107,
      "nroSerie": "192.168.40.179",
      "accesoSectorFk": 1,
      "puertaIngresoId": 2
    },
    {
      "id": 105,
      "nroSerie": "192.168.40.199",
      "accesoSectorFk": 1,
      "puertaIngresoId": 1
    },
    {
      "id": 95,
      "nroSerie": "192.168.40.201",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 88,
      "nroSerie": "192.168.40.202",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 89,
      "nroSerie": "192.168.40.203",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 90,
      "nroSerie": "192.168.40.204",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 91,
      "nroSerie": "192.168.40.205",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 92,
      "nroSerie": "192.168.40.206",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 93,
      "nroSerie": "192.168.40.207",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 94,
      "nroSerie": "192.168.40.208",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 96,
      "nroSerie": "192.168.40.209",
      "accesoSectorFk": 1,
      "puertaIngresoId": 3
    },
    {
      "id": 97,
      "nroSerie": "192.168.40.210",
      "accesoSectorFk": 1,
      "puertaIngresoId": 6
    },
    {
      "id": 98,
      "nroSerie": "192.168.40.211",
      "accesoSectorFk": 1,
      "puertaIngresoId": 6
    },
    {
      "id": 99,
      "nroSerie": "192.168.40.212",
      "accesoSectorFk": 1,
      "puertaIngresoId": 4
    },
    {
      "id": 101,
      "nroSerie": "192.168.40.213",
      "accesoSectorFk": 1,
      "puertaIngresoId": 4
    },
    {
      "id": 87,
      "nroSerie": "192.168.40.214",
      "accesoSectorFk": 1,
      "puertaIngresoId": 2
    },
    {
      "id": 100,
      "nroSerie": "192.168.40.215",
      "accesoSectorFk": 1,
      "puertaIngresoId": 4
    },
    {
      "id": 102,
      "nroSerie": "192.168.40.218",
      "accesoSectorFk": 1,
      "puertaIngresoId": 4
    },
    {
      "id": 104,
      "nroSerie": "192.168.40.219",
      "accesoSectorFk": 1,
      "puertaIngresoId": 4
    },
    {
      "id": 103,
      "nroSerie": "192.168.40.220",
      "accesoSectorFk": 1,
      "puertaIngresoId": 4
    }
  ]
}
*/