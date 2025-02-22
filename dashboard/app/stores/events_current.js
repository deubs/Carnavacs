import { create } from "zustand"

export const store_events_current = create((set)=> ({
    events_current: "loading",
    set_events_current: (value) => set({ events_current: value })
}))
