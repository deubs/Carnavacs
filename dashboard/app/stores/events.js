import { create } from "zustand"

export const store_events = create((set) => ({
    event_current: undefined,
    events_all: undefined,
    set_event_current: ( data ) => set((st) => ({
        event_current: data
    })),
    set_events_all: ( data ) => set((st) => ({
        events_all: data
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