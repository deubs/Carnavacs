import { create } from "zustand";

export const store_test = create((set)=>({
    state: false,
    set_state: (value) => set((st)=>({ state: value }))
}))