/*
toISOString
2023-11-22T10:30:00Z

toLocaleDateString - es-ES,
{
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
}dat
*/

export const event_entry_passed = ( turnstile ) => {
    return ({
    "turnstile_id": turnstile,
    "timestamp": new Date().toISOString(),
    "event": "entry",
    "ticket_id": Math.random(),
    "ticket_type": Math.random() < 0.8 ? "adult" : "children",
    "status": "success",
    "reason": "valid ticket"
})
}
export const event_entry_failed = ( turnstile ) => {
    return ({
    "turnstile_id": turnstile,
    "timestamp": new Date().toISOString(),
    "event": "entry",
    "ticket_id": Math.random(),
    "ticket_type": Math.random() < 0.8 ? "adult" : "children",
    "status": "failure",
    "reason": "invalid ticket, other night"
})
}
export const event_status = ( turnstile, status ) => {
    return ({
    "turnstile_id": turnstile,
    "timestamp": new Date().toISOString(),
    "event": "status",
    "status": status,
    "reason": "change status"
})
}
export const event_error = ( turnstile ) => {
    return ({
    "turnstile_id": turnstile,
    "timestamp": new Date().toISOString(),
    "event": "error",
    "status": "0",
    "reason": "bad request"
})
}