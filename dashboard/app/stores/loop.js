import { create } from "zustand";

export const store_loop = create((set)=> ({
    loop_status: false,
    count: 0,
    set_loop_status: (value) => set((st)=>({ loop_status: value })),
    count_increase: () => set((st)=>({ count: st.count + 1 }))
}))