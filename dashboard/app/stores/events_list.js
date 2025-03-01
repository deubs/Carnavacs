import { create } from "zustand"

export const store_events_list = create((set)=> ({
    events_list: "loading",
    set_events_list: (value) => set({ events_list: value })
}))
