import { create } from "zustand";

export const store_dashboard = create((set)=> ({ 
    container: "loading",
    set_container: (value) => set((st)=>({ container: value }))
})) 