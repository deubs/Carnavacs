import { create } from "zustand";

export const store_events_sector_stats = create((set)=> ({
    sector_stats: "loading",
    set_sector_stats: (value) => set((st)=>({ sector_stats: value }))
}))