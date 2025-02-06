import { create } from "zustand";

export const store_enviroment = create((set)=> ({
    enviroment: undefined,
    set_enviroment: (value) => set((st)=>({ enviroment: value }))
}))