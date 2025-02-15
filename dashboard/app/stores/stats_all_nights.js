import { create } from "zustand";

export const store_all_stats = create((set)=> ({
    nights: [],
    data: [],
    state: "loading",
    set_state: (value) => set((st)=>({ state: value })),
    set_nights: (value) => set((st)=>({ nights: value })),
    set_data: (value) => set((st)=>({ data: [...st.data, value] }))
})) 
