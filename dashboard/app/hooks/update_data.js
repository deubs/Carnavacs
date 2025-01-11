export const update_data = async (url) => {
    try {
        const r = await fetch(url)
        const rr = await r.json()
        if (rr.success) {
            return { data: rr.result }
        } else {
            throw new Error("events/stats")
        }
    } catch (error) {
        return { error: error }
    }
}