import { create } from "zustand";

export const store_enviroment = create((set)=> ({

    LOCAL_API_URL: undefined,
    API_URL: undefined,

    set_enviroment: (value) => set((st)=>({
        LOCAL_API_URL: value.LOCAL_API_URL,
        API_URL: value.API_URL
    }))
}))