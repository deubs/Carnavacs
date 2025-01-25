import { create } from "zustand"

export const store_events_current = create((set)=> ({
    events_current: false,
    set_events_current: (value) => set((st) => ({ events_current: value }))
}))
