import { NextResponse } from "next/server";
import { generate_token, check_token } from "./jsonwebtoken";
import { checkCredentials } from "./pseudodbusers";

const API_URL = process.env.NEXT_PUBLIC_APIURL_DEV || "http://192.168.40.100";

async function proxyToApi(endpoint) {
  try {
    const response = await fetch(`${API_URL}/${endpoint}`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.log(`Error proxying to API: ${API_URL}/${endpoint}`, error);
    return { success: false, error: error.message };
  }
}

const events = {
  "success": true,
  "message": null,
  "result": [
    {
      "id": 139,
      "fecha": "2025-01-04T21:00:00",
      "nombre": "1 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 140,
      "fecha": "2025-01-11T21:00:00",
      "nombre": "2 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 141,
      "fecha": "2025-01-18T21:00:00",
      "nombre": "3 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 142,
      "fecha": "2025-01-25T21:00:00",
      "nombre": "4 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 143,
      "fecha": "2025-02-01T21:00:00",
      "nombre": "5 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 144,
      "fecha": "2025-02-08T21:00:00",
      "nombre": "6 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 145,
      "fecha": "2025-02-15T21:00:00",
      "nombre": "7 Noche de Carnaval del Pais",
      "habilitado": false,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 150,
      "fecha": "2025-02-21T20:00:00",
      "nombre": "Eleccion de la Reina 2025",
      "habilitado": true,
      "showName": null
    },
    {
      "id": 146,
      "fecha": "2025-02-22T21:00:00",
      "nombre": "8 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 147,
      "fecha": "2025-03-01T21:00:00",
      "nombre": "9 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 148,
      "fecha": "2025-03-02T21:00:00",
      "nombre": "10 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 149,
      "fecha": "2025-03-03T21:00:00",
      "nombre": "11 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    }
  ]
}

const events_current = {
  "success": true,
  "message": null,
  "result": {
    "id": 146,
      "fecha": "2025-02-22T21:00:00",
      "nombre": "8 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
  }
}

const events_stats = {
  "success": true,
  "message": null,
  "result": {
    "eventId": 0,
    "totalTickets": 16660,
    "usedTickets": 638,
    "remainingTickets": 16022, 
    "totalGates": 0,
    "openGates": 0,
    "closedGates": 0,
    "gates": [
      {
        "gateId": 3,
        "gateName": "Ayacucho",
        "accessDevices": [
          {
            "deviceId": 88,
            "deviceName": "192.168.40.202",
            "peopleCount": 880
          },
          {
            "deviceId": 89,
            "deviceName": "192.168.40.203",
            "peopleCount": 1078
          },
          {
            "deviceId": 90,
            "deviceName": "192.168.40.204",
            "peopleCount": 192
          },
          {
            "deviceId": 91,
            "deviceName": "192.168.40.205",
            "peopleCount": 1095
          },
          {
            "deviceId": 92,
            "deviceName": "192.168.40.206",
            "peopleCount": 408
          },
          {
            "deviceId": 93,
            "deviceName": "192.168.40.207",
            "peopleCount": 703
          },
          {
            "deviceId": 94,
            "deviceName": "192.168.40.208",
            "peopleCount": 304
          },
          {
            "deviceId": 95,
            "deviceName": "192.168.40.201",
            "peopleCount": 856
          },
          {
            "deviceId": 96,
            "deviceName": "192.168.40.209",
            "peopleCount": 935
          }
        ]
      },
      {
        "gateId": 4,
        "gateName": "Maipu",
        "accessDevices": [
          {
            "deviceId": 99,
            "deviceName": "192.168.40.212",
            "peopleCount": 942
          },
          {
            "deviceId": 100,
            "deviceName": "192.168.40.215",
            "peopleCount": 1238
          },
          {
            "deviceId": 101,
            "deviceName": "192.168.40.213",
            "peopleCount": 4
          },
          {
            "deviceId": 102,
            "deviceName": "192.168.40.218",
            "peopleCount": 1084
          },
          {
            "deviceId": 103,
            "deviceName": "192.168.40.220",
            "peopleCount": 403
          },
          {
            "deviceId": 104,
            "deviceName": "192.168.40.219",
            "peopleCount": 1142
          }
        ]
      },
      {
        "gateId": 2,
        "gateName": "Proveedores",
        "accessDevices": [
          {
            "deviceId": 85,
            "deviceName": "192.168.40.181",
            "peopleCount": 1
          },
          {
            "deviceId": 86,
            "deviceName": "192.168.40.131",
            "peopleCount": 4
          },
          {
            "deviceId": 87,
            "deviceName": "192.168.40.214",
            "peopleCount": 841
          },
          {
            "deviceId": 106,
            "deviceName": "192.168.40.16",
            "peopleCount": 110
          }
        ]
      },
      {
        "gateId": 6,
        "gateName": "Puerta 8",
        "accessDevices": [
          {
            "deviceId": 97,
            "deviceName": "192.168.40.210",
            "peopleCount": 375
          },
          {
            "deviceId": 98,
            "deviceName": "192.168.40.211",
            "peopleCount": 634
          }
        ]
      },
      {
        "gateId": 1,
        "gateName": "Rocamora",
        "accessDevices": [
          {
            "deviceId": 105,
            "deviceName": "192.168.40.199",
            "peopleCount": 282
          }
        ]
      }
    ],
    "ticketStats": [
      {
        "total": 16022,
        "statusName": "Habilitado"
      },
      {
        "total": 163,
        "statusName": "Anulado"
      },
      {
        "total": 475,
        "statusName": "Ingreso"
      }
    ]
  }
}

const events_sectorStats = {
  "success": true,
  "message": null,
  "result": [
    {
      "id": 0,
      "name": "Popular",
      "total": "9002",
      "readed": "8416"
    },
    {
      "id": 0,
      "name": "SPBV",
      "total": "48",
      "readed": "44"
    },
    {
      "id": 0,
      "name": "SPESTE",
      "total": "32",
      "readed": "18"
    },
    {
      "id": 0,
      "name": "SPOESTE",
      "total": "312",
      "readed": "301"
    },
    {
      "id": 0,
      "name": "SSILLAS1A",
      "total": "122",
      "readed": "116"
    },
    {
      "id": 0,
      "name": "SSILLAS2A",
      "total": "165",
      "readed": "161"
    },
    {
      "id": 0,
      "name": "SSILLAS2B",
      "total": "181",
      "readed": "175"
    },
    {
      "id": 0,
      "name": "SSILLAS3A",
      "total": "175",
      "readed": "172"
    },
    {
      "id": 0,
      "name": "SSILLAS3B",
      "total": "205",
      "readed": "199"
    },
    {
      "id": 0,
      "name": "SSILLAS4A",
      "total": "386",
      "readed": "364"
    },
    {
      "id": 0,
      "name": "SSILLAS4B",
      "total": "389",
      "readed": "366"
    },
    {
      "id": 0,
      "name": "SSILLAS5A",
      "total": "169",
      "readed": "169"
    },
    {
      "id": 0,
      "name": "SSILLAS5B",
      "total": "219",
      "readed": "212"
    },
    {
      "id": 0,
      "name": "SSILLAS6A",
      "total": "55",
      "readed": "52"
    },
    {
      "id": 0,
      "name": "SSILLAS6B",
      "total": "135",
      "readed": "128"
    },
    {
      "id": 0,
      "name": "SSILLAS7A",
      "total": "21",
      "readed": "20"
    },
    {
      "id": 0,
      "name": "SSILLAS7B",
      "total": "26",
      "readed": "26"
    },
    {
      "id": 0,
      "name": "SVIP5B",
      "total": "98",
      "readed": "98"
    },
    {
      "id": 0,
      "name": "SVIP6A",
      "total": "68",
      "readed": "67"
    },
    {
      "id": 0,
      "name": "SVIP6B",
      "total": "64",
      "readed": "61"
    },
    {
      "id": 0,
      "name": "SVIPNEW",
      "total": "92",
      "readed": "91"
    },
    {
      "id": 0,
      "name": "SVIPRC",
      "total": "124",
      "readed": "104"
    },
    {
      "id": 0,
      "name": "SVIPRE",
      "total": "246",
      "readed": "188"
    },
    {
      "id": 0,
      "name": "SVIPRO",
      "total": "278",
      "readed": "238"
    },
    {
      "id": 0,
      "name": "SVIPTC",
      "total": "670",
      "readed": "631"
    },
    {
      "id": 0,
      "name": "SVIPTE",
      "total": "216",
      "readed": "203"
    },
    {
      "id": 0,
      "name": "SVIPTO",
      "total": "228",
      "readed": "218"
    }
  ]
}

const gates_gates = {
  "success": true,
  "message": null,
  "result": [
    {
      "id": 2,
      "nombre": "Puerta 2",
      "descripcion": "Piccini y Ayacucho",
      "sobreNombre": "Proveedores",
      "enabled": true
    },
    {
      "id": 3,
      "nombre": "Puerta 3",
      "descripcion": "Piccini y Maipu",
      "sobreNombre": "Ayacucho",
      "enabled": true
    },
    {
      "id": 4,
      "nombre": "Puerta 4",
      "descripcion": "Piccini y Chacabuco",
      "sobreNombre": "Maipu",
      "enabled": true
    },
    {
      "id": 6,
      "nombre": "Puerta 8",
      "descripcion": "Ayacucho y Estrada",
      "sobreNombre": "Puerta 8",
      "enabled": true
    }
  ]
}

const gates_devices = {
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
      "id": 85,
      "nroSerie": "192.168.40.181",
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

const gates_1 = {
  "success": true,
  "message": null,
  "result": {
    "id": 1,
    "nombre": "Puerta 1",
    "descripcion": "Piccini y Rocamora ",
    "sobreNombre": "Rocamora",
    "enabled": false
  }
}


export async function POST ( req ) {
  //console.log("header Auth: ", req.headers.Auth)
  try {
    const { event, data } = await req.json()
    
    switch ( event ) {
      case 1:
        // login
        try {
          const res = checkCredentials(data)
          
          if (res.login) { 
            const token = await generate_token(data.user)
            return NextResponse.json({ login: true, token })
          } else { 
            return NextResponse.json({ login: false }) }
          
        } catch (error) { 
          return NextResponse.json({ error }) 
        }
      case 2:
        try {
          const { url } = data
          const result = await proxyToApi(url)
          if (result.success) {
            return NextResponse.json(result.data)
          } else {
            console.log(`API proxy failed for ${url}, error: ${result.error}`)
            return NextResponse.json({ success: false, error: result.error })
          }
        } catch (error) {
          console.log(`Error in case 2: ${error}`)
          return NextResponse.json({ error })
        }
      
        default: return NextResponse.json({ r: "response default" })
    }
  } catch (error) {
    console.log(`Error en API local:
      event: ${event},
      data: ${data},
      error: error`)
      return NextResponse.json({ error: true })
  }
}

/*
const events_stats = {
    "success": true,
    "message": null,
    "result": {
      "eventId": 0,
      "totalTickets": 16660,
      "usedTickets": 638,
      "remainingTickets": 16022,
      "totalGates": 0,
      "openGates": 0,
      "closedGates": 0
    }}
*/
export async function GET ( req ) {
  const { eventId } = req.query;
  console.log(eventId) 
  return NextResponse.json({ error: "no get" })
}