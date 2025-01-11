import { create } from "zustand";

export const store_gates = create((set)=> ({
gate_01: {
    id: "Puerta 1",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_02: {
    id: "Puerta 2",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_03: {
    id: "Puerta 3",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_04: {
    id: "Puerta 4",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_05: {
    id: "Puerta 5",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_06: {
    id: "Puerta 6",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_07: {
    id: "Puerta 7",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_08: {
    id: "Puerta 8",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_09: {
    id: "Puerta 9",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_10: {
    id: "Puerta 10",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_11: {
    id: "Puerta 11",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_12: {
    id: "Puerta 12",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_13: {
    id: "Puerta 13",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_14: {
    id: "Puerta 14",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_15: {
    id: "Puerta 15",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_16: {
    id: "Puerta 16",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_17: {
    id: "Puerta 17",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_18: {
    id: "Puerta 18",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_19: {
    id: "Puerta 19",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_20: {
    id: "Puerta 20",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
gate_21: {
    id: "Puerta 21",
    status: 3,
    tickets: {
        passed: 0,
        failed: 0
    }
},
error_log: [],
add_error_log: (error) => set((state)=>({
    error_log: [...state.error_log, error]
})),

handlegate: (gate, event, value) => set((state)=>{
    
    if (event == "status") {
        return({ [gate]: { ...state[gate], status: value }})
    }
    if (event == "entry") {
        if (value == "success") {
            return ({ 
                [gate] : {
                    ...state[gate],
                    tickets: {
                        ...state[gate].tickets,
                        passed: state[gate].tickets.passed + 1
                    }
                }})
        }
        if (value == "failure") {
            return ({ 
                [gate] : {
                    ...state[gate],
                    tickets: {
                        ...state[gate].tickets,
                        failed: state[gate].tickets.failed + 1
                    }
                }})
        }
    }
})

}));