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
  return NextResponse.json({ error: "no get" })
}