import { create } from "zustand";

export const store_gates = create((set)=> ({
    gates: undefined,
    set_gates: (value) => set({ gates: value })
}))