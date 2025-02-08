import { create } from "zustand";

export const store_ticket_validate = create((set)=> ({
    m1: "SIN CARGA",
    m2: "SIN CARGA",
    info: "no info",
    set_data: (value) => set((st)=>({ 
        m1: value.m1, 
        m2: value.m2,
        info: value.info 
    }))
})) 