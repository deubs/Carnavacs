import { NextResponse } from "next/server";
import { generate_token, check_token } from "./jsonwebtoken";
import { checkCredentials } from "./pseudodbusers";


const _events = {
  "success": true,
  "message": null,
  "result": [
    {
      "id": 139,
      "fecha": "2025-01-04T21:00:00",
      "nombre": "1 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 140,
      "fecha": "2025-01-11T21:00:00",
      "nombre": "2 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 141,
      "fecha": "2025-01-18T21:00:00",
      "nombre": "3 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 142,
      "fecha": "2025-01-25T21:00:00",
      "nombre": "4 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 143,
      "fecha": "2025-02-01T21:00:00",
      "nombre": "5 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 144,
      "fecha": "2025-02-08T21:00:00",
      "nombre": "6 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
    },
    {
      "id": 145,
      "fecha": "2025-02-15T21:00:00",
      "nombre": "7 Noche de Carnaval del Pais",
      "habilitado": true,
      "showName": "CARNAVAL25G"
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

const _events_current = {
  "success": true,
  "message": null,
  "result": {
    "id": 139,
    "fecha": "2025-01-04T21:00:00",
    "nombre": "1 Noche de Carnaval del Pais",
    "habilitado": true,
    "showName": "CARNAVAL25G"
  }
}

const _events_stats = {
  "success": true,
  "message": null,
  "result": {
    "eventId": 0,
    "totalTickets": 1,
    "usedTickets": 0,
    "remainingTickets": 1,
    "totalGates": 0,
    "openGates": 0,
    "closedGates": 0,
    "gates": [
      {
        "gateId": 2,
        "gateName": "Proveedores",
        "accessDevices": [
          {
            "deviceId": 86,
            "deviceName": "192.168.40.131",
            "peopleCount": 16
          },
          {
            "deviceId": 106,
            "deviceName": "192.168.40.16",
            "peopleCount": 41
          },
          {
            "deviceId": 107,
            "deviceName": "192.168.40.179",
            "peopleCount": 1
          },
          {
            "deviceId": 87,
            "deviceName": "192.168.40.214",
            "peopleCount": 637
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
            "peopleCount": 2102
          }
        ]
      },
      {
        "gateId": 3,
        "gateName": "Ayacucho",
        "accessDevices": [
          {
            "deviceId": 95,
            "deviceName": "192.168.40.201",
            "peopleCount": 920
          },
          {
            "deviceId": 88,
            "deviceName": "192.168.40.202",
            "peopleCount": 1038
          },
          {
            "deviceId": 89,
            "deviceName": "192.168.40.203",
            "peopleCount": 1205
          },
          {
            "deviceId": 90,
            "deviceName": "192.168.40.204",
            "peopleCount": 738
          },
          {
            "deviceId": 91,
            "deviceName": "192.168.40.205",
            "peopleCount": 1275
          },
          {
            "deviceId": 92,
            "deviceName": "192.168.40.206",
            "peopleCount": 649
          },
          {
            "deviceId": 93,
            "deviceName": "192.168.40.207",
            "peopleCount": 825
          },
          {
            "deviceId": 94,
            "deviceName": "192.168.40.208",
            "peopleCount": 1222
          },
          {
            "deviceId": 96,
            "deviceName": "192.168.40.209",
            "peopleCount": 1080
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
            "peopleCount": 571
          },
          {
            "deviceId": 98,
            "deviceName": "192.168.40.211",
            "peopleCount": 1023
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
            "peopleCount": 1086
          },
          {
            "deviceId": 101,
            "deviceName": "192.168.40.213",
            "peopleCount": 17
          },
          {
            "deviceId": 100,
            "deviceName": "192.168.40.215",
            "peopleCount": 1311
          },
          {
            "deviceId": 102,
            "deviceName": "192.168.40.218",
            "peopleCount": 1184
          },
          {
            "deviceId": 104,
            "deviceName": "192.168.40.219",
            "peopleCount": 1372
          },
          {
            "deviceId": 103,
            "deviceName": "192.168.40.220",
            "peopleCount": 789
          }
        ]
      }
    ],
    "ticketStats": [
      {
        "total": 1,
        "statusName": "Habilitado"
      }
    ]
  }
}

const _gates = {
  "success": true,
  "message": null,
  "result": [
    {
      "id": 2,
      "nombre": "Puerta 2",
      "descripcion": "Piccini y Ayacucho",
      "sobreNombre": "Proveedore",
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

const _gates_id = {
  "success": true,
  "message": null,
  "result": {
    "id": 8,
    "nombre": "Puerta 5",
    "descripcion": "Piccini y España",
    "sobreNombre": null,
    "enabled": false
  }
}

const response_tickets_validate = {
    "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
    "title": "One or more validation errors occurred.",
    "status": 400,
    "errors": {
      "code": [
        "The code field is required."
      ]
    },
    "traceId": "00-00ac864bcf5a2f5895bd416d1c281a3a-7c58ea64194803e2-00"
}


export async function POST ( req ) {
    console.log("header Auth: ", req.headers.Auth)

    const { event, data } = await req.json()
    switch (event) {
        case 1:
            // login
            try {
                const res = checkCredentials(data)
                if (res.login) {
                    const token = await generate_token(data.user)
                    return NextResponse.json({ login: true, token })
                }
                return NextResponse.json({ login: false })
            } catch (error) {
                return NextResponse.json({ error })
            }
        case 3:
            // validacion de token jwt
            try {
                const { token } = data
                await check_token(token)
                return NextResponse.json({ r: "token correcto" })
            } catch (error) {
                return NextResponse.json({ error })
            }
        case 4:
            try {
                const { evento } = data
                
                if ( evento == "events") {
                    return NextResponse.json(_events)
                }
                if ( evento == "event_current") {
                    return NextResponse.json(_events_current)
                }
                if ( evento == "events_stats") {
                    return NextResponse.json(_events_stats)
                }
                if ( evento == "gates") {
                    return NextResponse.json(_gates)
                }
                if ( evento == "gates_id") {
                  return NextResponse.json(_gates_id)
              }
            } catch (error) {
                return NextResponse.json({ error })
            }
}
}

export async function GET ( req ) {
    return NextResponse.json({ error: "no get" })
}