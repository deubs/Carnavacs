import { create } from "zustand";

export const store_loop = create((set)=> ({
    loop_status: true,
    tick: 0,
    change_status: () => set((st)=>({ loop_status: !st.loop_status })),
    tick_increment: () => set((st)=>({ tick: st.tick + 1 }))
})) 