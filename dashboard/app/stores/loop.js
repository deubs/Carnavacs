import { create } from "zustand";

export const store_loop = create((set)=> ({
    loop_status: false,
    tick: 0, 
    change_status: (value) => set({ loop_status: value }),
    tick_increment: () => set((st)=>({ tick: st.tick + 1 }))
}))
