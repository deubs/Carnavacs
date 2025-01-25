import { create } from "zustand"

export const store_events_list = create((set)=> ({

    loaded: false, 
    data: undefined,

    set_data: (value) => set((st) => ({

        loaded: true,
        data: value
        
        }))
}))
