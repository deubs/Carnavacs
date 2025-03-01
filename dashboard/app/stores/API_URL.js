import { create } from "zustand";

export const store_API_URL = create((set)=> ({
    API_URL: undefined,
    set_API_URL: (value) => set({ API_URL: value })
}))