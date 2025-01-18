import { create } from "zustand";

export const store_notification = create((set)=> ({
    message: undefined,
    set_message: (value) => set((st)=>({ message: value }))
}))