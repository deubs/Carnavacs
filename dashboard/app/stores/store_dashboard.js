import { create } from "zustand";

export const store_dashboard = create((set)=> ({ 
    container: "home",
    set_container: (value) => set((st)=>({ container: value }))
})) 