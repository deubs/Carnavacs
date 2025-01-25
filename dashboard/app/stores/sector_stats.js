import { create } from "zustand";

export const store_sector_stats = create((set)=> ({
    data: undefined,
    set_data: (value) => set((st)=>({ data: value }))
}))