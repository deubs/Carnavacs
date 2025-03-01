export function get_nights (current_id, nights_array) {

    const regex = /\d+ Noche/
    const nights = []

    for (let event of nights_array) {

        const coincidencia = event.nombre.match(regex)
        if (event.id <= current_id) {
            const timestamp = new Date(event.fecha).getTime()
            const event_to_add = { name: coincidencia[0], id: event.id, timestamp }
            event_to_add.name = coincidencia ? coincidencia[0] : event.nombre
            nights.push(event_to_add)

        }
        
    }
    return nights
}