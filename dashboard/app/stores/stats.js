import { create } from "zustand"

export const store_stats = create((set)=> ({
    data: {
        totalTickets: "cargando...",
        usedTickets: "cargando...",
        remainingTickets: "cargando...",
    },
    set_data: (value) => set((st) => ({
        data: value
        }))
}))



/*
hourly_revenue: {
        20: 0,
        21: 0,
        22: 0,
        23: 0,
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    },

    sum_hourly_ticket : (hs) => set((st) => ({
        ...st,
        hourly_revenue: {
            ...st.hourly_revenue,
            [hs] : st.hourly_revenue[hs] + 1
        }
    })),
    sum_ticket: (ticket) => set((st) => ({
        ...st,
        tickets: {
            ...st.tickets,
            [ticket]: st.tickets[ticket] + 1
        }
    })),
*/