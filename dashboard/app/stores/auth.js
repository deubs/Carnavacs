import { create } from "zustand";

export const store_auth = create((set)=> ({
    authentication: undefined,
    set_authentication: (value) => set((st)=>({ authentication: value }))
}))