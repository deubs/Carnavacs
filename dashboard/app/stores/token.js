import { create } from "zustand";

export const store_token = create((set)=> ({
    token: undefined,
    set_token: (value) => set((st)=>({ token: value }))
}))