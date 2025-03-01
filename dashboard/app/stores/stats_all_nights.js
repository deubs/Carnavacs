import { create } from "zustand";

export const store_stats_all_nights = create((set)=> ({
    actually_night: {},
    previous_nights: [],
    state_data: 0,
    total_tickets: 0,
    set_actually_night: (value) => set({ actually_night: value }),
    add_night: (value) => set(st=>({ previous_nights: [...st.previous_nights, value]})),
    set_state_data: (value) => set({ state_data: value}),
    add_total_tickets: (value) => set(st=>({ total_tickets: st.total_tickets + value}))
}))
