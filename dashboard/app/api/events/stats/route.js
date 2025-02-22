import { NextResponse } from "next/server"

export async function GET (req, _) {
  const id = req.url.slice(-3)
  if (id == 139) return NextResponse.json({
    "success": true,
    "message": null,
    "result": {
      "eventId": 0,
      "totalTickets": 16500,
      "usedTickets": 638,
      "remainingTickets": 16022,
      "totalGates": 0,
      "openGates": 0,
      "closedGates": 0
    }})
    if (id == 140) return NextResponse.json({
        "success": true,
        "message": null,
        "result": {
          "eventId": 0,
          "totalTickets": 14730,
          "usedTickets": 638,
          "remainingTickets": 16022,
          "totalGates": 0,
          "openGates": 0,
          "closedGates": 0
        }})
        if (id == 141) return NextResponse.json({
            "success": true,
            "message": null,
            "result": {
              "eventId": 0,
              "totalTickets": 15768,
              "usedTickets": 638,
              "remainingTickets": 16022,
              "totalGates": 0,
              "openGates": 0,
              "closedGates": 0
            }})
        if (id == 142) return NextResponse.json({
          "success": true,
          "message": null,
          "result": {
            "eventId": 0,
            "totalTickets": 13910,
            "usedTickets": 13910,
            "remainingTickets": 0,
            "totalGates": 0,
            "openGates": 0,
            "closedGates": 0
          }})
          if (id == 143) return NextResponse.json({
            "success": true,
            "message": null,
            "result": {
              "eventId": 0,
              "totalTickets": 13218,
              "usedTickets": 13210,
              "remainingTickets": 8,
              "totalGates": 0,
              "openGates": 0,
              "closedGates": 0
            }})
            if (id == 144) return NextResponse.json({
              "success": true,
              "message": null,
              "result": {
                "eventId": 0,
                "totalTickets": 15117,
                "usedTickets": 13708,
                "remainingTickets": 1409,
                "totalGates": 0,
                "openGates": 0,
                "closedGates": 0
              }})
            if (id == 145) return NextResponse.json({
              "success": true,
              "message": null,
              "result": {
                "eventId": 0,
                "totalTickets": 14683,
                "usedTickets": 13067,
                "remainingTickets": 1616,
                "totalGates": 0,
                "openGates": 0,
                "closedGates": 0
              }})
            if (id == 146) return NextResponse.json({
              "success": true,
              "message": null,
              "result": {
                "eventId": 0,
                "totalTickets": 9612,
                "usedTickets": 221,
                "remainingTickets": 9391,
                "totalGates": 0,
                "openGates": 0,
                "closedGates": 0
              }})
  return NextResponse.json({ error: "no get" })
}