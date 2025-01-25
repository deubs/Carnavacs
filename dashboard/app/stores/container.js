import { create } from "zustand";

export const store_container = create((set)=> ({
    container: "dashboard",
    set_container: (value) => set((st)=>({ container: value }))
}))