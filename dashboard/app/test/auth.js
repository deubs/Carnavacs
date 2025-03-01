import { create } from "zustand";

export const store_authentication = create((set)=> ({
    token: undefined,
    authenticated: undefined,
    set_token: (value) => set((st)=>({ token: value, authenticated: true }))
}))