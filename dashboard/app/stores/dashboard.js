import { create } from "zustand";

export const store_dashboard = create((set)=> ({
    dashboard: "home",
    set_dashboard: (value) => set((st)=>({ dashboard: value }))
}))