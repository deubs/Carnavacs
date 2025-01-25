import { create } from "zustand";

export const store_gates = create((set)=> ({
    gates: false,
    set_gates: (value) => set((st)=>({ gates: value }))
}))