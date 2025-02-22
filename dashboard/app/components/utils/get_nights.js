export function get_nights (current_id, nights_array) {

    const regex = /\d+ Noche/
    const nights = []

    for (let event of nights_array) {
        const coincidencia = event.nombre.match(regex)
        if (event.id < current_id) {
            if (coincidencia) {
                nights.push({ name: coincidencia[0], id: event.id })
            } else {
                nights.unshift({ name: event.nombre, id: event.id })
            }
        }
    }
    return nights
}