import { create } from "zustand";

export const store_sector_stats = create((set)=> ({
    sector_stats: false,
    set_sector_stats: (value) => set((st)=>({ sector_stats: value }))
}))