import { create } from "zustand"

export const store_events_stats = create((set)=> ({
    events_stats: false, 
    set_events_stats: (value) => set((st) => ({ events_stats: value }))
}))
 