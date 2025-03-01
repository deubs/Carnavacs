import { create } from "zustand"

export const store_event_id = create((set)=> ({
    event_id: undefined,
    set_event_id: (value) => set({ event_id: value })
}))
