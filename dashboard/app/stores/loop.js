import { create } from "zustand";

export const store_loop = create((set)=> ({
    loop_status: false,
    tick: 0,
    set_loop_status: (value) => set((st)=>({ loop_status: value })),
    tick_increment: () => set((st)=>({ tick: st.tick + 1 }))
})) 