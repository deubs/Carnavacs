import { create } from "zustand";

export const store_ticket_validate = create((set)=> ({
    m1: "SIN CARGA",
    m2: "SIN CARGA",
    set_data: (value) => set((st)=>({ 
        m1: value.m1, 
        m2: value.m2 
    }))
})) 