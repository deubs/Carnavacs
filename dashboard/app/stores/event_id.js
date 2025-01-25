import { create } from "zustand"

export const store_event_id = create((set)=> ({
    event_id: false,
    set_event_id: (value) => set((st) => ({ event_id: value }))
}))
