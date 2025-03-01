export const data_parse = (date) => {
    const data_parsed = new Date(date).toLocaleDateString("es-ES", { year: "numeric", month: "long", day: "2-digit"})
    //console.log(date, data_parsed)
    return data_parsed
}