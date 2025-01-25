import { create } from "zustand";

export const store_API_URL = create((set)=> ({ 
    API_URL: false,
    set_API_URL: (value) => set((st)=>({ API_URL: value }))
}))