import { create } from "zustand";

export const store_stats_all_nights = create((set)=> ({
    previous_nights: [],
    add_night: (value) => set((st)=>({ previous_nights: [...st.previous_nights, value]})),
})) 
  