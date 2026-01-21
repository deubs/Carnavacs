export function get_nights (current_id, nights_array) {

    const regex = /\d+ Noche/
    const nights = []

    for (let event of nights_array) {

        const coincidencia = event.nombre.match(regex)
        if (event.id <= current_id) {
            const timestamp = new Date(event.fecha).getTime()
            const name = coincidencia ? coincidencia[0] : event.nombre
            const event_to_add = { name, id: event.id, timestamp }
            nights.push(event_to_add)

        }
        
    }
    return nights
}